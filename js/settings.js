document.addEventListener('DOMContentLoaded', function () {
    const links = document.querySelectorAll('.settings-link');
    const sections = document.querySelectorAll('.settings-section');

    links.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault();

            sections.forEach(section => {
                section.classList.remove('active');
            });

            const sectionId = link.getAttribute('data-section');
            document.getElementById(sectionId).classList.add('active');
        });
    });

    // Show the profile section by default
    document.getElementById('profile').classList.add('active');
});
