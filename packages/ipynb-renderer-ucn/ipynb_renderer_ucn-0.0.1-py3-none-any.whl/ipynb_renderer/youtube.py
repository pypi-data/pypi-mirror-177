from ensure import ensure_annotations
from ipynb_renderer.custom_exception import InvalidURLException
from ipynb_renderer.logger import logger
from IPython import display
from py_youtube import Data


@ensure_annotations
def get_time(URL: str) -> int:
    def _verify_vid_id_len(vid_id, _expected_len=11):
        len_of_vid_id = len(vid_id)
        if len_of_vid_id != _expected_len:
            raise InvalidURLException(
                f"Invalid video id with length: {len_of_vid_id}, expected: {_expected_len}"
            )

    try:
        split_val = URL.split("=")
        if len(split_val) > 3:
            raise InvalidURLException
        if "watch" in URL:
            if "&t" in URL:
                vid_id, time = split_val[-2][:-2], int(split_val[-1][:-1])
                _verify_vid_id_len(vid_id)
                logger.info(f"video starts at: {time}")
                return time
            else:
                vid_id, time = split_val[-1], 0
                _verify_vid_id_len(vid_id)
                logger.info(f"video starts at: {time}")
                return time
        else:
            if "=" in URL and "?t" in URL:
                vid_id, time = split_val[0].split("/")[-1][:-2], int(split_val[-1])
                _verify_vid_id_len(vid_id)
                logger.info(f"video starts at: {time}")
                return time
            else:
                vid_id, time = URL.split("/")[-1], 0
                _verify_vid_id_len(vid_id)
                logger.info(f"video starts at: {time}")
                return time
    except Exception:
        raise InvalidURLException


@ensure_annotations
def render_youtube(URL: str, width: int = 780, height: int = 600) -> str:
    try:
        data = Data(URL).data()
        if data["publishdate"]:
            time = get_time(URL)
            vid_ID = data["id"]
            embed_URL = f"https://www.youtube.com/embed/{vid_ID}?start={time}"
            logger.info(f"embed URL: {embed_URL}")
            iframe = f"""<iframe
            width="{width}" height="{height}"
            src="{embed_URL}"
            title="YouTube video player"
            frameborder="0"
            allow="accelerometer;
            autoplay; clipboard-write;
            encrypted-media; gyroscope;
            picture-in-picture" allowfullscreen>
            </iframe>
            """
            display.display(display.HTML(iframe))
            return "success"
        else:
            raise InvalidURLException
    except Exception as e:
        raise e
