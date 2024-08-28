document.querySelector('#discordModal .modal-close, #closeModal').addEventListener('click', function () {
    document.getElementById('discordModal').classList.remove('is-active');
  });
  document.querySelector('[href="#discordModal"]').addEventListener('click', function (event) {
    event.preventDefault();
    document.getElementById('discordModal').classList.add('is-active');
  });