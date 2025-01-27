import ssl
import time
import undetected_chromedriver as uc
from typing_extensions import Optional

ssl._create_default_https_context = ssl._create_unverified_context


class Scraper:
    driver = None

    @property
    def options(self):
        options_ = uc.ChromeOptions()
        options_.headless = True  # For view window use False
        return options_

    def create_driver(self):
        self.driver = uc.Chrome(options=self.options, use_subprocexss=True)
        self.driver.set_page_load_timeout(30)
        return self.driver

    def close_driver(self):
        self.driver.quit()

    def restart_driver(self):
        if self.driver:
            self.driver.close()
        time.sleep(1)
        self.create_driver()

    def get_page(self, url: str, click_: Optional[list] = None):
        self.create_driver()
        try:
            self.driver.get(url)
            time.sleep(1)
            if click_:
                self.driver_click(click_)
                time.sleep(2)
            html = self.driver.page_source
            return html
        except Exception as e:
            print(f'DRIVER Exception {e}')
            self.close_driver()
            return self.get_page(url)

    def driver_click(self, click_: Optional[list] = None) -> None:
        """
        :param click_: mast be list of params like click=[By.ID, "category-menu-button"]
            firs params set 'By.' type search, second params set name search
        :return: None
        """
        btn = self.driver.find_element(*click_)
        print(f'btn {btn}')
        btn.click()
        time.sleep(0.3)

    def driver_page_source(self):
        try:
            html = self.driver.page_source
        except Exception as e:
            print(f'DRIVER Exception {e}')
            html = False
        return html
