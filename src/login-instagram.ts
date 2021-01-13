import puppeteer from "puppeteer";
import fs from "fs";

const instagram_url = "https://www.instagram.com/";

export {};

const main = async (browser: puppeteer.Browser) => {
  const page = await browser.newPage();
  const wait = async (target: string) => {
    await page.waitFor(target);
  };
  const input = async (target_selector: string, content: string) => {
    await page.type(target_selector, content);
  };

  const loginSelector =
    "#loginForm > div > div:nth-child(1) > div > label > input";

  const passSelector =
    "#loginForm > div > div:nth-child(2) > div > label > input";
  const buttonSelector = "#loginForm > div > div:nth-child(3) > button";

  await wait(loginSelector);
  await wait(passSelector);
  await wait(buttonSelector);
  await input(loginSelector, process.env.USER!!);
  await input(passSelector, process.env.PASS!!);
  await page.click(buttonSelector);
};

(async () => {
  const browser = await puppeteer.launch({
    // headless: process.env.HEADLESS && false || true
    headless: false,
  });

  // const page = await browser.newPage()
  try {
    await main(browser);
  } catch (e) {
    console.log(`err: ${e}`);
  } finally {
    // await browser.close();
  }
})();
