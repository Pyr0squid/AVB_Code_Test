/* App bootstrap/wiring */

import { fetchNames } from "./api.js";
import { renderContactList } from "./render.js";
import { handleContactClick } from "./events.js";
import {
  openAddContactModal,
  closeAddContactModal,
  handleAddContactSubmit,
  handleAddEmailModal,
} from "./events.js";

document.addEventListener("DOMContentLoaded", async () => {
  const contacts = await fetchNames();
  renderContactList(contacts, handleContactClick);
});

document.addEventListener("DOMContentLoaded", () => {
  document
    .getElementById("create-contact-btn")
    .addEventListener("click", openAddContactModal);

  document
    .getElementById("cancel-btn")
    .addEventListener("click", closeAddContactModal);

  document
    .getElementById("create-contact-form")
    .addEventListener("submit", handleAddContactSubmit);
});

document.addEventListener("DOMContentLoaded", () => {
  document
    .getElementById("add-email-btn")
    .addEventListener("click", handleAddEmailModal);
});
