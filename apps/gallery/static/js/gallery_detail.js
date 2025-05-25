document.addEventListener('DOMContentLoaded', function() {
  const select = document.getElementById('city-filter');
  const form = document.querySelector(`form[action="${galleryDetailURL}"]`);
  var elem = document.querySelector('#masonry-container');
  let msnry;

  // Function to initialize Masonry after images are loaded
  function initializeMasonry() {
    // Destroy existing Masonry instance if it exists
    if (msnry) {
      msnry.destroy();
    }

    msnry = new Masonry( elem, {
      itemSelector: '.gallery_product',
      columnWidth: '.gallery_product'
    });
     // Layout after Masonry is initialized
    msnry.layout();
  }

  // Load images first
  imagesLoaded(elem).on('always', function() {
    initializeMasonry();
  });

  form.addEventListener('submit', function(event) {
    // Prevent form submission.
    event.preventDefault();
    const value = select.value;

    if (value.toLowerCase() === 'all') {
      document.querySelectorAll('.gallery_product').forEach(item => {
        // Callback to display all images and re-layout
        $(item).show(300, function() {
          item.classList.remove('hidden');
          msnry.layout();
        });
      });
    } else {
      document.querySelectorAll('.gallery_product').forEach(item => {
        if (!item.classList.contains(value)) {
          // Callback to hide unrelated images and re-layout
          $(item).hide(500, function() {
            item.classList.add('hidden');
            msnry.layout();
          });
        } else {
          // Callback to display related images and re-layout
          $(item).show(500, function() {
            item.classList.remove('hidden');
            msnry.layout();
          });
        }
      });
    }
  });

  // Trigger form submission once animation is finished.
  select.addEventListener('change', function() {
    form.dispatchEvent(new Event('submit'));
  });
});
