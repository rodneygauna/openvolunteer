// Functionality for the alert banners

/* banner functions */
var fadeOutInterval;

function showBanner() {
  var banner = document.getElementsByClassName("alert")[0];
  banner.style.display = "flex";
  resetHideTimer();
}

function hideBanner() {
  var banner = document.getElementsByClassName("alert")[0];
  banner.style.opacity = 1;
  fadeOutInterval = setInterval(function () {
    if (banner.style.opacity > 0) {
      banner.style.opacity -= 0.1;
    } else {
      clearInterval(fadeOutInterval);
      banner.style.display = "none";
    }
  }, 60);
}

function resetHideTimer() {
  clearInterval(fadeOutInterval);
  fadeOutInterval = setTimeout(hideBanner, 5000);
}

var bannerSuccess = document.getElementsByClassName("alert alert-success")[0];
if (bannerSuccess) {
  resetHideTimer();
}
