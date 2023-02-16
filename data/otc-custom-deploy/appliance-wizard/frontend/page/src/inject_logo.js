var logo = undefined;

async function fetch_logo() {
  let res = await fetch("./logo.svg")
  let text = await res.text();

  return text;
}

export function inject_logo() {
  fetch_logo().then(l => {
    Array.from(
      document.getElementsByClassName("otc-logo")
    ).forEach((item, i) => {
      item.innerHTML = l;
    });
  })
}
