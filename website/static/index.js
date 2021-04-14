const mobileBtn = document.getElementById('mobile-menu-btn')
          nav = document.querySelector('#nav')
          mobileBtnExit = document.getElementById('mobile-x-btn');
          
    mobileBtn.addEventListener('click', () => {
      nav.classList.add('menu-btn');
    })

    mobileBtnExit.addEventListener('click', () => {
      nav.classList.remove('menu-btn');
    })