// Close modal with "X"
document.querySelectorAll('#discordModal .modal-close, #closeModal').forEach(function (element) {
  element.addEventListener('click', function () {
    document.getElementById('discordModal').classList.remove('is-active');
  });
});

// Close modal with button
document.querySelectorAll('[href="#discordModal"]').forEach(function (link) {
  link.addEventListener('click', function (event) {
    event.preventDefault();
    document.getElementById('discordModal').classList.add('is-active');
  });
});
