import time

from quickverifyimg.log.logger import get_logger
from quickverifyimg.quick_verify import QuickVerify
logger = get_logger(__name__)

if __name__ == '__main__':
    quick_v = QuickVerify(verify_img_dir='./images/verify_img', backgroup_img_path='./images/background.png', crop_place={"size": (0.815, 1.0), "offset": (0.175, 0)},  quick_verify=True)
    start_time = time.time()
    verify_engine_list = [
        ('ac_tpl', 0.99),
        ('hist', 0.995)
    ]
    ret = quick_v.mutliple_engine_verify(
        img_dir="./images/screenshot", verify_engine_list=verify_engine_list, match_rate_threshold=0.8)

    logger.info("结果：{}, 通过率：{}".format(ret['result'], ret["final_match_rate"]))
    logger.info('总耗时：{}'.format(time.time() - start_time))
    logger.info('失败截图：{}'.format(ret["verify_fail_screenshots"]))
    logger.info('非背景图总数：{}'.format(ret["available_screenshot_num"]))
    logger.info('非背景图：{}'.format(ret["available_screenshots"]))