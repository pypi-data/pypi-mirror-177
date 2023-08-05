import os

import cv2
from natsort import ns, natsorted

import copy

from quickverifyimg.log.logger import get_logger
from quickverifyimg.aircv_utils import match_image
from quickverifyimg.cv2_utils import compare_hist, ssim
from quickverifyimg.hash_utils import getHash_similarity_p, getHash_similarity_d, getHash_similarity_a
from quickverifyimg.psnr import get_psnr_similar
from quickverifyimg.thread_utils import MyThread
logger = get_logger(__name__)

switcher = {
    'ac_tpl': match_image,
    'hist': compare_hist,
    'ssim': ssim,
    'psnr': get_psnr_similar,
    'hash_p': getHash_similarity_p,
    'hash_a': getHash_similarity_a,
    'hash_d': getHash_similarity_d,
}

class QuickVerify():
    def __init__(self, verify_img_dir, backgroup_img_path, crop_place=None, quick_verify=False, background_num_after_start_max=30):
        """
        :param verify_img_dir: 对照图片集文件路径
        :param backgroup_img_path: 背景图路径
        :param crop_place: 需要裁剪的位置： {"size": (0.815, 1.0), "offset": (0.175, 0)}  # 去掉顶部0.175位置
        :param quick_verify: 是否快速校验，即不对已校验过的对照集图片继续校验
        :param background_num_after_start_max: 特效开始后最大背景图数
        """
        self.quick_verify = quick_verify
        self.crop_place = crop_place
        self.verify_img_dir = verify_img_dir
        self.backgroup_img_path = backgroup_img_path
        self.background_num_after_start_max = background_num_after_start_max
        self.backgroup_img = cv2.imread(self.backgroup_img_path)
        # 获取用来校验的图片集
        self.verify_images_file_list = os.listdir(self.verify_img_dir)
        self.verify_images_file_list = natsorted(self.verify_images_file_list,
                                            alg=ns.PATH)  # 要加alg=ns.PATH参数才和windows系统名称排序一致
        self.verify_images = []
        self.verify_images_name = []
        for file_name in self.verify_images_file_list:
            file_path = os.path.join(verify_img_dir, file_name)
            if not os.path.isfile(file_path):
                continue
            self.verify_images.append(cv2.imread(file_path))
            self.verify_images_name.append(file_name)

            # 如果校验图片目录中没有图片，直接返回false
        if len(self.verify_images) < 1:
            logger.error(f"no image in verify_images_dir {verify_img_dir}")
            raise Exception("no image in verify_img_dir")

    def verify_img(self, img_list, verify_img_index, verify_type=1,compare_threshold=0.99):
        """
        检验图片
        :param img_list: 待校验图片集
        :param verify_img_index: 对照图片集开始顺序
        :param verify_type: 校验图片算法
        :param compare_threshold: 校验图片阈值
        :return:
        """
        is_start = False
        background_num_after_start = 0
        background_num_after_start_max = self.background_num_after_start_max
        cut_match_index = -1
        available_screenshot_num = 0  # 非背景图的截图的数量
        match_times = 0  # 跟verify_images_dir对比，相似度超过阈值的图片数量
        verify_fail_screenshots = []
        available_screenshot_list = []
        for img_path in img_list:
            img = cv2.imread(img_path)
            if self._similiar_with_background(img, self.backgroup_img, verify_type):
                if not is_start:  # 特效未开始，但截图跟背景图一样，应该是截图早了，判断下一张即可
                    continue
                elif background_num_after_start > background_num_after_start_max:  # 特效已开始，而截图跟背景图一样，如果连续出现30次，认为是特效已经展示完了
                    logger.info(
                        f"background_num_after_start > {background_num_after_start_max}, break this verify {img_path}")
                    break
                else:
                    logger.info(f"found a background img with {img_path}")
                    background_num_after_start += 1  # 特效已开始，而截图跟背景图一样，未达到连续30次，只记录次数，说不定是特效效果就这样
                    continue
            else:
                available_screenshot_list.append(img_path)
                available_screenshot_num += 1
                background_num_after_start = 0  # 截图跟背景图不一样，刷新次数

            best_matching_name =''
            best_matching_similiar = 0
            verify_images = self.verify_images[verify_img_index:len(self.verify_images)]
            verify_images_name = self.verify_images_name[verify_img_index:len(self.verify_images_name)]
            tmp_verify_images = copy.deepcopy(verify_images)
            for index, verify_img in enumerate(verify_images):
                # 因为截图和校验图都是连续的，所以如果有校验通过了的校验图，下次校验时可以跳过此次之前的图片
                if self.quick_verify and index < cut_match_index:
                    continue
                is_similiar, similiar = self._is_image_similiar(img, verify_img, verify_type,
                                                             match_image_threshold=compare_threshold)
                if is_similiar:
                    logger.debug(f"{img_path} match {verify_images_name[index]}, similiar: {similiar}")
                    if not self.quick_verify:
                        tmp_verify_images.pop(index)
                    cut_match_index = index
                    match_times += 1
                    is_start = True
                    best_matching_name = ""
                    break
                else:
                    if best_matching_similiar < similiar:
                        best_matching_similiar = similiar
                        best_matching_name = self.verify_images_name[index]
            if best_matching_name:
                verify_fail_screenshots.append(img_path)
                logger.debug(
                    f"{os.path.basename(img_path)} unmatch any images, threshold: {compare_threshold}, "
                    f"best_matching_name: {best_matching_name}"
                    f"similiar : {similiar}"
                )
        return {
           'available_screenshot_num':available_screenshot_num,
           "match_times": match_times,
           "verify_fail_screenshots":verify_fail_screenshots,
            "available_screenshots":available_screenshot_list
        }

    def verify_perf(self, img_dir, verify_type, compare_threshold, match_rate_threshold):
        img_list = []
        effect_screenshot = os.listdir(img_dir)
        effect_screenshot.sort(key=lambda x: int(x[:-4]) if x[:-4].isdigit() else x[:-4])  # 去掉后缀名来排序
        for file_name in effect_screenshot:
            file_path = os.path.join(img_dir, file_name)
            if not os.path.isfile(file_path):
                continue
            img_list.append(file_path)

        # 先查找特效的第一张图片
        start_index = 0
        for img_path in img_list:
            img = cv2.imread(img_path)
            if self._similiar_with_background(img, self.backgroup_img, verify_type):
                start_index += 1
            else:
                break
        logger.debug(f'特效开始的第一张图片：{img_list[start_index]}')
        img_list = img_list[start_index: len(img_list)]
        # 10张图片就开一个线程去查询
        img_threshold = 10
        thread_list = []
        available_screenshot_sum = 0
        match_times_sum = 0
        verify_fail_screenshots_all = []
        available_screenshot_list_all = []
        for i in range(0, len(img_list), img_threshold):
            all_list_temp = img_list[i:i + img_threshold]
            # 对照集的开始校验的图片序号
            verify_index = 0
            if self.quick_verify:
                # 如果是快速校验，则往前偏移10张照片开始校验
                verify_index = i -10
                if verify_index < 0:
                    verify_index = 0
            thread = MyThread(self.verify_img, args=(all_list_temp, verify_index), kwargs={'verify_type':verify_type, 'compare_threshold':compare_threshold})
            thread.start()
            thread_list.append(thread)
        for t in thread_list:
            t.join()
            ret = t.get_result()
            available_screenshot_list_all.extend(ret["available_screenshots"])
            available_screenshot_sum += ret["available_screenshot_num"]
            match_times_sum += ret["match_times"]
            verify_fail_screenshots_all.extend(ret["verify_fail_screenshots"])

        # 计算匹配率 (达到相似度阈值的截图数量 / 非背景图的截图数量)
        final_match_rate = 0
        if available_screenshot_sum:
            final_match_rate = match_times_sum / available_screenshot_sum
        ret = {
            'final_match_rate':final_match_rate,
            'verify_fail_screenshots':verify_fail_screenshots_all,
            'available_screenshot_num':available_screenshot_sum,
            'available_screenshots':available_screenshot_list_all
        }
        if final_match_rate >= match_rate_threshold:
            ret['result'] = True
        else:
            ret['result'] = False
        return ret


    def _similiar_with_background(self, img, background_image, verify_type):
        is_similiar, _ = self._is_image_similiar(img, background_image, verify_type, 0.998)
        if is_similiar:
            return True
        else:
            return False

    def _is_image_similiar(self, image1, image2, verify_type, match_image_threshold=0.99):
        image1_crop = image1
        image2_crop = image2
        # crop_place = {"size": (0.815, 1.0), "offset": (0.175, 0)}
        if self.crop_place:
            image1_crop = self.crop_frame(image1, **self.crop_place)
            image2_crop = self.crop_frame(image2, **self.crop_place)
        get_similiar = switcher.get(verify_type, "")
        similar = get_similiar(image1_crop, image2_crop)
        # print('相似度为：{}'.format(similar))
        if match_image_threshold > similar:
            return False, similar
        else:
            return True, similar

    def crop_frame(self, frame, size=(), offset=()):
        """
        获取图片的指定区域
        :param frame: 图像的narray
        :param size: 需要识别的区域的大小， 百分比
        :param offset: 需要识别的区域的左上角坐标点位置， 百分比
        """
        origin_h, origin_w = frame.shape[:2]
        if size[0] < 1 or size[1] < 1 or offset[0] < 1 or offset[1] < 1:
            skip_rect = {"startX": int(origin_w * offset[1]), "startY": int(origin_h * offset[0]),
                         "endX": int(origin_w * (offset[1] + size[1])),
                         "endY": int(origin_h * (offset[0] + size[0]))}
        else:
            skip_rect = {"startX": int(offset[1]), "startY": int(offset[0]),
                         "endX": int(offset[1] + size[1]),
                         "endY": int(offset[0] + size[0])}
        frame_crop = frame[skip_rect["startY"]:skip_rect["endY"], skip_rect["startX"]:skip_rect["endX"]]
        # print(
        #     '裁剪图片：start_x: {}, start_y: {}, end_x: {}, end_y: {}'.format(skip_rect["startX"], skip_rect["startY"],
        #                                                                  skip_rect["endX"], skip_rect["endY"]))
        return frame_crop

    def mutliple_engine_verify(self, img_dir, verify_engine_list, match_rate_threshold):
        """
        多算法调用
        :param img_dir:
        :param verify_type_list: {(1, 0.99), (2, 0.98}
        :param match_rate_threshold:
        :return:
        """
        thread_list = []
        sum = 0
        available_screenshot_set = set()
        verify_fail_screenshots_set =set()
        logger.info(f"使用匹配算法和阈值列表：{verify_engine_list}")
        for i in range(0, len(verify_engine_list)):
            thread = MyThread(self.verify_perf, args=(img_dir, verify_engine_list[i][0], verify_engine_list[i][1], match_rate_threshold), kwargs={})
            thread.start()
            thread_list.append(thread)
        for t in thread_list:
            t.join()
            verify_result = t.get_result()
            if verify_result['result']:
                ret = {
                    'result': verify_result['result'],
                    'final_match_rate':verify_result["final_match_rate"],
                    'verify_fail_screenshots': verify_result["verify_fail_screenshots"],
                    'available_screenshot_num':verify_result["available_screenshot_num"],
                    'available_screenshots': verify_result["available_screenshots"]
                }
                return ret
            else:
                sum += verify_result["available_screenshot_num"]
                # 取非背景图交集
                if available_screenshot_set:
                    available_screenshot_set = set(verify_result["available_screenshots"]) & available_screenshot_set
                else:
                    available_screenshot_set = set(verify_result["available_screenshots"])
                # 取失败截图交集
                if verify_fail_screenshots_set:
                    verify_fail_screenshots_set = verify_fail_screenshots_set & set(verify_result["verify_fail_screenshots"])
                else:
                    verify_fail_screenshots_set = set(verify_result["verify_fail_screenshots"])

        final_rate = len(verify_fail_screenshots_set)/len(available_screenshot_set)
        ret = {
            'final_match_rate': final_rate,
            'verify_fail_screenshots': verify_fail_screenshots_set,
            'available_screenshot_num': len(available_screenshot_set),
            'available_screenshots':available_screenshot_set
        }
        if final_rate > match_rate_threshold:
            ret['result'] = True
        else:
            ret['result'] = False
        return ret