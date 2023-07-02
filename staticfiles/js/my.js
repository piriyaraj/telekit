function imgError(image) {
  image.onerror = "";
  image.src = "/static/images/nopic.jpg";
  return true;
}

(async () => {
  "use strict";

  const delay = (ms) => new Promise((res) => setTimeout(res, ms));
  const $ = (x) => document.querySelector(x);

  await delay(100);
  const elem = $(".dialog-box");

  if (elem) {
    elem.style.visibility = "hidden";
    await delay(1000 + 4000 * Math.random());
    console.log(new Date().toLocaleTimeString() + ": Clicked");
    $(".here-button").click();
  }
})();
