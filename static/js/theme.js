(function() {
    window.addEventListener('load', () => {
        document.querySelector('a#dark-mode').addEventListener('click', e => {
            e.preventDefault();
            toggleTheme();
        });
    });

    function checkTheme() {
        const theme = localStorage.getItem('theme') || 'default';
        document.querySelector('html').classList.add(theme);
    }

    function toggleTheme() {
        const themes = ['default', 'dark'];
        let theme = localStorage.getItem('theme') || 'default';

        if (!themes.includes(theme))
            theme = 'default';

        themes.forEach(t => document.querySelector('html').classList.toggle(t));
        localStorage.setItem('theme', themes[(themes.indexOf(theme)+1) % 2]);
    }

    checkTheme();
})();
