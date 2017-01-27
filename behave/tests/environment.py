from utils import get_chrome_webdriver


def before_all(context):
    """Set global variables."""
    context.browser = get_chrome_webdriver()


def after_all(context):
    """Quit selenium browser."""
    context.browser.quit()


def after_step(context, step):
    if step.status == "failed":
        import ipdb
        ipdb.post_mortem(step.exc_traceback)
