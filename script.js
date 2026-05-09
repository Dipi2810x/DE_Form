// Form submission
const form = document.getElementById('form');
if (form) {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = {
      name: form.name.value,
      email: form.email.value
    };
    await fetch('/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });
    form.reset();
  });
}

// Live dashboard
const socket = io();
const responseList = document.getElementById('responseList');

if (responseList) {
  socket.on('initialData', (data) => {
    data.forEach(addResponse);
  });

  socket.on('newResponse', (data) => {
    addResponse(data);
  });

  function addResponse(data) {
    const li = document.createElement('li');
    li.textContent = `${data.name} (${data.email})`;
    responseList.appendChild(li);
  }
}