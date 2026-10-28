// Progressive enhancement only: all forms work without JavaScript.
document.addEventListener('submit', function (event) {
  const form = event.target;
  if (form.dataset.submitting === 'true') {
    event.preventDefault();
    return;
  }
  form.dataset.submitting = 'true';
  form.setAttribute('aria-busy', 'true');
  form.querySelectorAll('button[type="submit"]').forEach(button => {
    button.disabled = true;
  });
});
window.addEventListener('pageshow', function () {
  document.querySelectorAll('form[data-submitting]').forEach(form => {
    delete form.dataset.submitting;
    form.removeAttribute('aria-busy');
    form.querySelectorAll('button[type="submit"]').forEach(button => {
      button.disabled = false;
    });
  });
});
