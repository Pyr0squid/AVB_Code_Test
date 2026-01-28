/* contains fetch/http calls */

const API_BASE = "/api";

export async function fetchNames() {
    const res = await fetch(`${API_BASE}/names`);
    return res.json();
}

export async function fetchContact(id) {
    const res = await fetch(`${API_BASE}/retrieve/${id}`);
    return res.json();
}

export async function createContact(data) {
    return fetch(`${API_BASE}/add/contact`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
}

export async function createAddress(data) {
    return fetch(`${API_BASE}/add/address`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
}

export async function updateContact(data) {
    return fetch(`${API_BASE}/update`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
}

export async function deleteContact(id) {
    return fetch(`${API_BASE}/delete/contact`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id })
    });
}

export async function deleteAddress(data) {
    return fetch(`${API_BASE}/delete/address`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
}