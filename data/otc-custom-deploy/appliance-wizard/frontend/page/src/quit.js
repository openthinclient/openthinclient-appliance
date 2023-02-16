export function quit() {
  fetch("http://localhost:4321/api/v1/deactivate").then();
  fetch("http://localhost:4321/api/v1/term_frontend").then();
}
