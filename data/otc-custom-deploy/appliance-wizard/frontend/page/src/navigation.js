import { clear_errors } from './actions.js';

const pages = document.querySelectorAll(".page:not(.unavailable)");
var current = -1;

export function goto(i) {
  if (i < 0) return

  clear_errors();

  for (let j = 0; j < pages.length; j++) {
    if (j < i) {
      pages[j].classList.remove("future")
      pages[j].classList.add("past")
    } else if (j > i) {
      pages[j].classList.remove("past")
      pages[j].classList.add("future")
    }

    pages[j].classList.remove("present")
  }
  current = i;

  pages[current].classList.add("present")
  pages[current].classList.remove("past")
  pages[current].classList.remove("future")
  setTimeout(() => {
    pages[current].querySelector("[focus-on-enter]")?.focus()
  }, 200)
}

export function next() {
  clear_errors();

  if (current >= pages.length -1) return
  if (current >= 0) {
    pages[current].classList.remove("present")
    pages[current].classList.add("past")
  }

  current++;

  pages[current].classList.remove("future")
  pages[current].classList.add("present")
  setTimeout(() => {
    pages[current].querySelector("[focus-on-enter]")?.focus()
  }, 200)
}

export function back() {
  clear_errors();

  if (current <= 0) return

  pages[current].classList.remove("present")
  pages[current].classList.add("future")

  current--;

  pages[current].classList.remove("past")
  pages[current].classList.add("present")
  setTimeout(() => {
    pages[current].querySelector("[focus-on-enter]")?.focus()
  }, 200)
}

goto(0)
