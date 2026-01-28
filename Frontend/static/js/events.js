/* Event listeners and handlers */

import { fetchContact, updateContact, createContact, createAddress, deleteContact, deleteAddress } from "./api.js";
import { setEditing, setSelectedContact, state } from "./state.js";
import { renderContactDetails } from "./render.js";

export async function handleContactClick(id) {
    const contact = await fetchContact(id);
    setSelectedContact(contact);

    // Package handlers to pass to renderer
    const handlers = {
        onSave: async (event) => {
          await handleEditSubmit(event, handlers);
        },
        onDelete: async () => {
          console.log("Deleting contact ID:", contact.id);
          try {
            setEditing(false);
            const response = await deleteContact(contact.id);
            if (response.ok) {
              window.location.reload();
            } else {
              alert("Delete failed on server.");
            }
          } catch (err) {
            console.error("Network error during delete:", err);
          }
        },
        onCancel: () => {
          setEditing(false);
          renderContactDetails(state.selectedContact, handlers);
        },
        onEdit: () => {
          setEditing(true);
          renderContactDetails(state.selectedContact, handlers);
        },
        onAddEmail: () => {
          const container = document.getElementById("new-emails-container");
          const inputHtml = `<div class="email-row"><input type="email" placeholder="new@email.com" class="email-row input" /></div>`;
          container.insertAdjacentHTML('beforeend', inputHtml);
        },
        onDeleteEmail: async (email) => {
          // The confirm() method pauses execution and returns true if 'OK' is clicked
          const confirmed = confirm(`Are you sure you want to delete the address "${email}"?`);
      
          if (confirmed) {
            try {
              // Calls the API to remove the specific address
              await deleteAddress({ id: contact.id, address: email });
          
              // Refresh the local state to reflect the change
              const updated = await fetchContact(contact.id);
              setSelectedContact(updated);
          
              // Re-render the view with the updated list
              renderContactDetails(updated, handlers);
            } catch (err) {
              console.error("Error deleting address:", err);
              alert("Could not delete address. Please try again.");
            }
          }
        }
    };

    renderContactDetails(contact, handlers);
}

export function openAddContactModal() {
  document
    .getElementById("modal-overlay")
    .classList.remove("hidden");
}

function resetAddContactForm() {
  // clear fields in add contact form
  const form = document.getElementById("create-contact-form");
  form.reset();

  // clear email list if there is one
  const emailList = document.getElementById("email-list");
  if (emailList) {
    emailList.innerHTML = "";
  }
}

export function closeAddContactModal() {
  resetAddContactForm();
  
  document
    .getElementById("modal-overlay")
    .classList.add("hidden");
}

export async function handleAddContactSubmit(event) {
  event.preventDefault();

  // retrieve email address from form and validate them
  const email = [...document.querySelectorAll(".email-row input")]
    .map(input => input.value.trim())
    .filter(email => email !== "");

  const invalid = email.some(e => !e.includes("@"));
  if (invalid) {
    alert("One or more email addresses are invalid");
    return;
  }

  // retrieve other contact details
  const form = event.target;

  // load contact details into json
  const data = {
    first_name: form.first_name.value,
    middle_name_init: form.middle_name_init.value || null,
    last_name: form.last_name.value,
    birthday: form.birthday.value || null,
    e_addresses: email
  };

  // query create contact API
  await createContact(data);

  // close modal
  closeAddContactModal();

  //reload sidebar
  window.location.reload();
}

// modal add email button handler
export function handleAddEmailModal() {
  const emailList = document.getElementById("email-list");

  const html_to_insert = `<div class="email-row"> 
                            <input 
                              type="email" 
                              placeholder="example@email.com" 
                              class="email-row input"
                            /> </div>`;

  emailList.insertAdjacentHTML('beforeend', html_to_insert);
}

// edit view submit handler
export async function handleEditSubmit(event, handlers) {
  event.preventDefault();

  // retrieve contact details minus email addresses
  const form = event.target;
  const contact = state.selectedContact;

  // load contact details into json
  const data = {
    id: contact.id,
    first_name: form.first_name.value || contact.first_name,
    middle_name_init: form.middle_name_init.value || contact.middle_name_init || null,
    last_name: form.last_name.value || contact.last_name,
    birthday: form.birthday.value || contact.birthday || null
  };

  // query create contact API
  await updateContact(data);

  // retrieve email address from form and validate them
  const newEmailInputs = [...document.querySelectorAll("#new-emails-container .email-row input")];
  const newEmails = newEmailInputs
    .map(input => input.value.trim())
    .filter(email => email !== "" && email.includes("@"));

  if (newEmails.length > 0) {
    for (const email of newEmails) {
      await createAddress({ id: contact.id, address: email });
    }
  }

  // update local state
  const updated = await fetchContact(state.selectedContact.id);
  setSelectedContact(updated);

  // re-render contact details
  setEditing(false);
  renderContactDetails(updated, handlers);
}