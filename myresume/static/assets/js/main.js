
(function () {
  "use strict";

  /**
   * Header toggle
   */
  const headerToggleBtn = document.querySelector('.header-toggle');

  function headerToggle() {
    document.querySelector('#header').classList.toggle('header-show');
    headerToggleBtn.classList.toggle('bi-list');
    headerToggleBtn.classList.toggle('bi-x');
  }
  if (headerToggleBtn) {
    headerToggleBtn.addEventListener('click', headerToggle);
  }

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navmenu a').forEach(navmenu => {
    navmenu.addEventListener('click', () => {
      if (document.querySelector('.header-show')) {
        headerToggle();
      }
    });
  });

  /**
   * Toggle mobile nav dropdowns
   */
  document.querySelectorAll('.navmenu .toggle-dropdown').forEach(navmenu => {
    navmenu.addEventListener('click', function (e) {
      e.preventDefault();
      this.parentNode.classList.toggle('active');
      this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
      e.stopImmediatePropagation();
    });
  });

  /**
   * Preloader
   */
  const preloader = document.querySelector('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      setTimeout(() => {
        preloader.remove();
        const siteContent = document.querySelector('#site-content');
        if (siteContent) {
          siteContent.style.visibility = 'visible';
          siteContent.style.opacity = '1';
        }
      }, 3000);
    });
  }

  /**
   * Scroll top button
   */
  const scrollTop = document.querySelector('.scroll-top');

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
  }
  if (scrollTop) {
    scrollTop.addEventListener('click', (e) => {
      e.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }
  window.addEventListener('load', toggleScrollTop);
  document.addEventListener('scroll', toggleScrollTop);

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    if (typeof AOS !== 'undefined') {
      AOS.init({
        duration: 600,
        once: false,
        mirror: true
      });
    }
  }
  window.addEventListener('load', aosInit);

  /**
   * Init typed.js
   */
  const selectTyped = document.querySelector('.typed');
  if (selectTyped && typeof Typed !== 'undefined') {
    let typed_strings = selectTyped.getAttribute('data-typed-items');
    typed_strings = typed_strings.split(',');
    new Typed('.typed', {
      strings: typed_strings,
      loop: true,
      typeSpeed: 50,
      backSpeed: 25,
      backDelay: 1000
    });
  }

  /**
   * Initiate Pure Counter
   */
  if (typeof PureCounter !== 'undefined') {
    new PureCounter();
  }

  /**
   * Animate the skills items on reveal
   */
  const skillsAnimation = document.querySelectorAll('.skills-animation');
  if (typeof Waypoint !== 'undefined') {
    skillsAnimation.forEach((item) => {
      new Waypoint({
        element: item,
        offset: '80%',
        handler: function () {
          const progress = item.querySelectorAll('.progress .progress-bar');
          progress.forEach(el => {
            el.style.width = el.getAttribute('aria-valuenow') + '%';
          });
        }
      });
    });
  }

  /**
   * Initiate glightbox
   */
  if (typeof GLightbox !== 'undefined') {
    GLightbox({ selector: '.glightbox' });
  }

  /**
   * Init isotope layout and filters
   */
  if (typeof Isotope !== 'undefined' && typeof imagesLoaded !== 'undefined') {
    document.querySelectorAll('.isotope-layout').forEach(function (isotopeItem) {
      let layout = isotopeItem.getAttribute('data-layout') ?? 'masonry';
      let filter = isotopeItem.getAttribute('data-default-filter') ?? '*';
      let sort = isotopeItem.getAttribute('data-sort') ?? 'original-order';

      let initIsotope;
      imagesLoaded(isotopeItem.querySelector('.isotope-container'), function () {
        initIsotope = new Isotope(isotopeItem.querySelector('.isotope-container'), {
          itemSelector: '.isotope-item',
          layoutMode: layout,
          filter: filter,
          sortBy: sort
        });
      });

      isotopeItem.querySelectorAll('.isotope-filters li').forEach(function (filters) {
        filters.addEventListener('click', function () {
          isotopeItem.querySelector('.isotope-filters .filter-active').classList.remove('filter-active');
          this.classList.add('filter-active');
          initIsotope.arrange({ filter: this.getAttribute('data-filter') });
          aosInit();
        });
      });
    });
  }

  /**
   * Correct scrolling position upon page load for URLs containing hash links.
   */
  window.addEventListener('load', function () {
    if (window.location.hash && document.querySelector(window.location.hash)) {
      setTimeout(() => {
        const section = document.querySelector(window.location.hash);
        const scrollMarginTop = getComputedStyle(section).scrollMarginTop;
        window.scrollTo({
          top: section.offsetTop - parseInt(scrollMarginTop),
          behavior: 'smooth'
        });
      }, 100);
    }
  });

  /**
   * Navmenu Scrollspy
   */
  const navmenulinks = document.querySelectorAll('.navmenu a');

  function navmenuScrollspy() {
    navmenulinks.forEach(navmenulink => {
      if (!navmenulink.hash) return;
      const section = document.querySelector(navmenulink.hash);
      if (!section) return;
      const position = window.scrollY + 200;
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        document.querySelectorAll('.navmenu a.active').forEach(link => link.classList.remove('active'));
        navmenulink.classList.add('active');
      } else {
        navmenulink.classList.remove('active');
      }
    });
  }
  window.addEventListener('load', navmenuScrollspy);
  document.addEventListener('scroll', navmenuScrollspy);

})();

/**
 * Portfolio Section
 */
document.addEventListener('DOMContentLoaded', () => {
  const navButtons = document.querySelectorAll('.nav-button');
  const portfolioItems = document.querySelectorAll('.portfolio-items');

  navButtons.forEach(button => {
    button.addEventListener('click', () => {
      const target = button.getAttribute('data-target');

      portfolioItems.forEach(item => item.classList.remove('active'));
      navButtons.forEach(btn => btn.classList.remove('active'));

      document.getElementById(target)?.classList.add('active');
      button.classList.add('active');
    });
  });

  document.getElementById('shipping')?.classList.add('active');
  navButtons[0]?.classList.add('active');
});

/**
 * Custom Mouse Cursor
 */


const cursorInner = document.querySelector('.cursor-inner');
const cursorOuter = document.querySelector('.cursor-outer');

if (cursorInner && cursorOuter) {  // Check if elements exist
    document.addEventListener('mousemove', (e) => {
        let mouseX = e.clientX;
        let mouseY = e.clientY;

        // Immediate move for outer circle
        cursorOuter.style.left = `${mouseX}px`;
        cursorOuter.style.top = `${mouseY}px`;

        // Delay effect for inner circle
        requestAnimationFrame(() => {
            cursorInner.style.left = `${mouseX}px`;
            cursorInner.style.top = `${mouseY}px`;
        });
    });

    // Apply hover effect on target elements
    const hoverTargets = [...document.querySelectorAll('a'), ...document.querySelectorAll('.cursor-pointer')];

    hoverTargets.forEach(el => {
        el.addEventListener('mouseenter', () => {
            cursorInner.classList.add('cursor-hover');
            cursorOuter.classList.add('cursor-hover');
        });
        el.addEventListener('mouseleave', () => {
            cursorInner.classList.remove('cursor-hover');
            cursorOuter.classList.remove('cursor-hover');
        });
    });

    // Show the cursor elements on page load
    cursorInner.style.visibility = 'visible';
    cursorOuter.style.visibility = 'visible';

    // Click effect for the inner cursor
    document.addEventListener('mousedown', () => {
        cursorInner.style.transform = 'scale(1.5)';
        setTimeout(() => {
            cursorInner.style.transform = 'scale(1)';
        }, 200); // Reset after 200ms
    });
}


/**
 * Skill Bars Animation
 */
document.addEventListener('DOMContentLoaded', () => {
  const bars = document.querySelectorAll('.bar');
  bars.forEach((bar) => {
    const pctElement = bar.querySelector('.pct');
    const data = JSON.parse(bar.dataset.bar);

    bar.style.backgroundColor = data.color;
    bar.style.width = '0%';

    setTimeout(() => {
      bar.style.width = data.percentage + '%';

      setTimeout(() => {
        pctElement.style.opacity = 1;
        pctElement.textContent = data.percentage + '%';
      }, 2000);
    }, 500);
  });
});
