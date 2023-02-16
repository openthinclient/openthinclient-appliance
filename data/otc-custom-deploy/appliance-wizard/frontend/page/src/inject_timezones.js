async function fetch_timezones() {
  let res = await fetch('http://localhost:4321/api/v1/timezones');
  let timezones = (await res.json()).timezones;
  return timezones;
}

export function inject_timezones() {
  fetch_timezones().then(t => {
    Array.from(
      document.getElementsByClassName("inject-timezones")
    ).forEach((item, i) => {
      t.forEach((timezone, j) => {
        item.innerHTML += `<option value="${timezone}">${timezone}</option>`
      });
    });
  });
}
