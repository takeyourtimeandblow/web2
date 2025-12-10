const select = document.querySelector('.navigation_select');
if (select) {
  select.addEventListener('change', function() {
    window.location.href = this.value;
  });
}
