from abc import ABCMeta, abstractmethod
from ultralytics import YOLO
import math
from collections import deque
import os

import numpy as np
import cv2
 
 
class PanoramaProjector(metaclass=ABCMeta):
    @staticmethod
    def parse_mapping_style(mapping_style):
        mode = 1
        if isinstance(mapping_style, str):
            if mapping_style == 'perspective':
                mode = 1
            elif mapping_style == 'stereographic':
                mode = 1 / 2
            elif mapping_style == 'equidistant':
                mode = 0
            elif mapping_style == 'equisolid_angle':
                mode = -1 / 2
            elif mapping_style == 'orthographic':
                mode = -1
        elif isinstance(mapping_style, tuple):
            f, n = mapping_style
            if f == 'tan':
                mode = 1 / n
            elif f == 'id':
                mode = 0
            elif f == 'sin':
                mode = -1 / n
        else:
            mode = mapping_style
 
        return mode
 
    def __call__(self, panorama, lon=0, lat=0, fov=105, width=800, height=600, mapping_style=1, fov_mode=True):
        lon = np.radians(lon)
        lat = np.radians(lat)
        if fov_mode:
            fov = np.radians(fov)
 
        [panorama_height, panorama_width, _] = panorama.shape
        spmap = self._spmap(lon, lat, fov, width, height, mapping_style=mapping_style, fov_mode=fov_mode)
        pxmap = self._pxmap(spmap, panorama_width, panorama_height)
        return cv2.remap(panorama,
                         pxmap[0].astype(np.float32),
                         pxmap[1].astype(np.float32),
                         cv2.INTER_CUBIC,
                         borderMode=cv2.BORDER_WRAP,
                         )
 
    @staticmethod
    def r(angle, mapping_style=1):
        # projection fomula of distance
        if mapping_style == 0:
            return angle
        elif mapping_style > 0:
            return np.tan(mapping_style * angle) / mapping_style
        else:
            return np.sin(mapping_style * angle) / mapping_style
 
    @staticmethod
    def r_inv(d, mapping_style=1):
        if mapping_style == 0:
            inv = d
        elif mapping_style > 0:
            inv = np.arctan(mapping_style * d) / mapping_style
        else:
            inv = np.arcsin(mapping_style * d) / mapping_style
 
        if isinstance(inv, np.ndarray):
            inv[inv > np.pi / 2] = float('inf')
 
        return inv
 
    def _spmap(self, lon, lat, fov, width, height, mapping_style=1, fov_mode=True):
        xyz = self._3dmap(fov, width, height, mapping_style=mapping_style, fov_mode=fov_mode)
 
        # x軸周りに -(pi/2-lat) 回転
        rx = np.array([[1, 0, 0],
                       [0, np.sin(lat), np.cos(lat)],
                       [0, -np.cos(lat), np.sin(lat)]])
        # z軸周りに -(pi/2-lon) 回転
        rz = np.array([[np.sin(lon), np.cos(lon), 0],
                       [-np.cos(lon), np.sin(lon), 0],
                       [0, 0, 1]])
 
        xyz = xyz.reshape([height * width, 3]).T
        xyz = np.dot(rx, xyz)
        xyz = np.dot(rz, xyz)
 
        # 球面上の座標(x, y, z)を緯度lonと経度latに変換する
        lon_map = np.arctan2(xyz[1], xyz[0])  # 東経
        lat_map = np.arcsin(xyz[2])  # 北緯
 
        lon_map = lon_map.reshape([height, width])
        lat_map = lat_map.reshape([height, width])
 
        return lon_map, lat_map
 
    def _3dmap(self, fov, width, height, mapping_style=1, fov_mode=True):
        # 画像の座標(i, j)から回転前の球面上の座標(x, y, z)への対応を作る
 
        # 像の範囲を求める
        if fov_mode:
            # fovが視野角を意味するモード
            # 視野角fovから(像の対角線の長さ)/2=r(fov/2)に変換
            fov = self.r(fov / 2, mapping_style=mapping_style)
        a = fov / np.sqrt(width ** 2 + height ** 2)
        vw = width * a  # z=1平面上の幅の半分
        vh = height * a
 
        # 画像の座標(i, j)から像の中の座標への対応
        x = np.tile(np.linspace(-vw, vw, width), [height, 1])
        y = np.tile(np.linspace(-vh, vh, height), [width, 1]).T
 
        # 球面上の座標に変換するための倍率を計算
        # self._r_inv(a2) が像の中心からの角度になっている
        a2 = np.sqrt(x ** 2 + y ** 2)
        a2 = np.sin(self.r_inv(a2, mapping_style=mapping_style)) / a2
 
        # 球面上の座標(x, y, z)を求める
        x *= a2
        y *= a2
        z = np.sqrt(1 - x ** 2 - y ** 2)
 
        return np.stack((x, y, z), axis=2)  # shape = height, width, 3
 
    @abstractmethod
    def _pxmap(self, sperical_map, panorama_width, panorama_height):
        pass
 
    def inverse(self, perspective, lon=0, lat=0, fov=105, panorama_width=8192, panorama_height=4096,
                mapping_style=1, fov_mode=True):
        lon = np.radians(lon)
        lat = np.radians(lat)
        if fov_mode:
            fov = np.radians(fov)
 
        [height, width, _] = perspective.shape
        pxmap_inv = self._pxmap_inv(panorama_width, panorama_height)
        x, y = self._spmap_inv(pxmap_inv, lon, lat, fov, width, height,
                               mapping_style=mapping_style, fov_mode=fov_mode)
 
        panorama = cv2.remap(perspective,
                             x.astype(np.float32),
                             y.astype(np.float32),
                             cv2.INTER_CUBIC,
                             borderMode=cv2.BORDER_TRANSPARENT)
 
        return panorama
 
    def _spmap_inv(self, pxmap_inv, lon, lat, fov, width, height, mapping_style=1, fov_mode=True):
        xyz, panorama_width, panorama_height = self._3dmap_inv(pxmap_inv, lon, lat)
 
        if fov_mode:
            fov = self.r(fov / 2, mapping_style=mapping_style)
        a = fov / np.sqrt(width ** 2 + height ** 2)
        vw = width * a
        vh = height * a
 
        # 裏側を取り除く
        f = xyz[2] <= 0  # filter
        xyz[:, f] = [[float('inf')], [float('inf')], [-1]]
 
        a2 = self.r(np.arccos(xyz[2]), mapping_style=mapping_style) / np.sqrt(xyz[0] ** 2 + xyz[1] ** 2)
        xyz *= a2
 
        xyz[0] += vw
        xyz[1] += vh
 
        xyz /= a*2
 
        x = xyz[0].reshape([panorama_height, panorama_width])
        y = xyz[1].reshape([panorama_height, panorama_width])
 
        return x, y
 
    def _3dmap_inv(self, pxmap_inv, lon, lat):
        lon_map, lat_map = pxmap_inv
        panorama_height = lon_map.shape[0]
        panorama_width = lat_map.shape[1]
 
        # x = sin(pi/2 - lat) * cos(lon) = cos(lat) * cos(lon)
        # y = sin(pi/2 - lat) * sin(lon) = cos(lat) * sin(lon)
        # z = cos(pi/2 - lat)            = sin(lat)
        x = np.cos(lat_map) * np.cos(lon_map)
        y = np.cos(lat_map) * np.sin(lon_map)
        z = np.sin(lat_map)
        xyz = np.stack((x, y, z), axis=2)
 
        # x軸周りに (pi/2-lat) 回転
        rxi = np.array([[1,           0,            0],
                        [0, np.sin(lat), -np.cos(lat)],
                        [0, np.cos(lat),  np.sin(lat)]])
        # z軸周りに (pi/2-lon) 回転
        rzi = np.array([[np.sin(lon), -np.cos(lon), 0],
                        [np.cos(lon),  np.sin(lon), 0],
                        [          0,            0, 1]])
 
        xyz = xyz.reshape([panorama_height * panorama_width, 3]).T
        xyz = np.dot(rzi, xyz)
        xyz = np.dot(rxi, xyz)
 
        return xyz, panorama_width, panorama_height
 
    @abstractmethod
    def _pxmap_inv(self, panorama_width, panorama_height):
        pass
 
 
# equirectangular
class EquirecProjector(PanoramaProjector):
    def _pxmap(self, spmap, panorama_width, panorama_height):
        i = panorama_width * (1 / 2 - spmap[0] / 2 / np.pi)
        j = panorama_height * (1 / 2 - spmap[1] / np.pi)
 
        return i, j
 
    def _pxmap_inv(self, width, height):
        lon_map = np.tile(np.linspace(np.pi, -np.pi, width), [height, 1])
        lat_map = np.tile(np.linspace(np.pi/2, -np.pi/2, height), [width, 1]).T
 
        return lon_map, lat_map
 
 
class PanoramaViewer(metaclass=ABCMeta):

    def __init__(self, image_path, projector,model, loncnt=0, latcnt=0, width=800, height=600, fov=105, mapping_style='perspective'):
        # self._image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        self._image = image_path
        self._projector = projector
        self._model = model
        self._width = width
        self._height = height
        self._mapping_style = projector.parse_mapping_style(mapping_style)
        self._d = self._projector.r(np.radians(fov) / 2, mapping_style=self._mapping_style)
        self._stride = np.degrees(self._projector.r_inv(self._d / 10))
        self._lon = loncnt * self._stride
        self._lat = latcnt * self._stride
 
    def __call__(self):
        image = self._projector(self._image, self._lon, self._lat, self._d, self._width, self._height,
                                mapping_style=self._mapping_style, fov_mode=False)
        cv2.imshow("image", image)
        # self._model(image,show=True)
        
        # self.detect_contour(image)
        # self.detect_feature_point(image)
        return
    
    def ball_place(self,img,flag):
        image = self._projector(img, self._lon, self._lat, self._d, self._width, self._height,
                        mapping_style=self._mapping_style, fov_mode=False)

        if flag : 
            result = self._model(image,imgsz=320,verbose=False)
        else:
            result = self._model(image,imgsz=640,verbose=False)

        # result[0]からResultsオブジェクトを取り出す
        result_object = result[0]
        # バウンディングボックスの座標を取得
        bounding_boxes = result_object.boxes.xyxy
        # クラスIDを取得
        class_ids = result_object.boxes.cls
        # クラス名の辞書を取得
        class_names_dict = result_object.names
        for box, class_id in zip(bounding_boxes, class_ids):
            class_name = class_names_dict[int(class_id)]
            if class_name == 'sports ball':
                x1,y1,x2,y2 = box
                return x1,y1,x2,y2
        return -1,-1,-1,-1

class VideoViewer():
    def __init__(self, video_path,projector,model, width=1200, height=600,pict_width = 800,pict_height =600):
        self._cap = cv2.VideoCapture(video_path)
        self._projector = projector
        self._model = model
        self._width = width
        self._height = height
        self._pict_width = pict_width
        self._pict_height = pict_height
        self.default_ball_siz = 50
        self.queue = deque()
        self.que_sum = 0
        self.que_limit = 3

    def __call__(self):

        while True:
            is_continue = True
            is_first = True
            ret = False
            img = np.zeros((self._height, self._width, 3), np.uint8)
            loncnt = 0 
            latcnt = 0 # [-13,13]
            lastmag = 1 #拡大倍率
            ball_find = True
            while True:
                ret, img = self._cap.read()
                #方針最初だけ全探索して後は差分だけ最初は一番いいのを選ぶ
                cost = math.inf

                if is_first:
                    xmi = ymi = xma = yma = 0#微調整用
                    besti = -1
                    bestj = -1
                    pano = PanoramaViewer(img, self._projector,self._model)
                    for i in range(8):
                        for j in range(5):
                            pano._lon =  6 * i * pano._stride
                            pano._lat = 6 * (j-2) * pano._stride
                            a,b,c,d = pano.ball_place(img,ball_find)
                            # pano()
                            # cv2.waitKey(0)
                            if a == -1 and b ==  -1 and c == -1 and d == -1:
                                continue
                            #ボールの中心と画像の中心のユークリッド距離
                            nowcost = math.sqrt((self._pict_width/2-(a+c)/2)*(self._pict_width/2-(a+c)/2)+(self._pict_height/2-(b+d)/2)*(self._pict_height/2-(b+d)/2))
                            print(nowcost)
                            if nowcost < cost:
                                xmi = a
                                ymi = b
                                xma = c
                                yma = d
                                besti = i
                                bestj = j
                                cost = nowcost

                    # #微調整
                    xmid = (xma + xmi)/2
                    ymid = (yma + ymi)/2

                    loncnt = 6 *besti +((self._pict_width/2 -xmid)*6/self._pict_width)
                    latcnt = 6 * (bestj-2) +((xmid -self._pict_width/2-ymid)*6/self._pict_width)

                    pano._lon = loncnt * pano._stride
                    pano._lat = latcnt * pano._stride

                    ball_siz = max(1.0,(abs(xma-xmi) + abs(yma - ymi))/2)
                    self.queue.append(ball_siz)
                    self.que_sum += ball_siz

                    lastmag = (self.que_sum/len(self.queue))/self.default_ball_siz
                    pano._d *= (self.que_sum/len(self.queue))/self.default_ball_siz


                    pano()
                    cv2.waitKey(0)
                    is_first = False
                else:
                    viewer = PanoramaViewer(img, self._projector,self._model,loncnt,latcnt)
                    a,b,c,d = viewer.ball_place(img,ball_find)
                    if a == -1 and b == -1 and c == -1 and d == -1:
                        viewer._d *= lastmag
                        ball_find = False
                    else:
                        xmid = (a + c)/2
                        ymid = (b + d)/2
                        loncnt += ((self._pict_width/2-xmid)*6/self._pict_width)
                        latcnt += ((self._pict_height/2-ymid)*6/self._pict_height)
                        ball_siz = (abs(a-c) + abs(b-d))/2
                        self.queue.append(ball_siz)
                        self.que_sum += ball_siz
                        while(len(self.queue) > self.que_limit):
                            self.que_sum -= self.queue[0]
                            self.queue.popleft()
                        viewer._d *= (self.que_sum/len(self.queue))/self.default_ball_siz
                        lastmag = (self.que_sum/len(self.queue))/self.default_ball_siz
                        ball_find = True

                    viewer._lon = loncnt * viewer._stride
                    viewer._lat = latcnt * viewer._stride
                    viewer()

                if ret == False:
                    is_continue = False
                    break
                # # qを押すと再生終了
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    is_continue = False
                    break
          
            #再生終了
            if is_continue == False:
                break

        self._cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    model = YOLO('yolov8n.pt')
    projector = EquirecProjector()
    # viewer = PanoramaViewer('pingpongball.png', projector,model)
    # viewer()
    video = VideoViewer('./Videos/soccer.mov',projector,model)
    video()

    
    
 