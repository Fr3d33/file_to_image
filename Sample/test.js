async function fetchEmoji() {
  const response = await fetch("https://emojihub.yurace.pro/api/random");
  const emoji = await response.json();
  console.log(emoji);
}

fetchEmoji();
