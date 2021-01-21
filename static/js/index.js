document.addEventListener('DOMContentLoaded', () => {
    /**
     * @desc CSRF protection when using GET links
     *
     * Make links with the 'link_as_form' class act as a <submit> button
     * This is needed, for instance, for CSRF on GET requests
     *
     * @example
     * <form method="POST" action="/logout">
     *     <input type="hidden" value="aaa-bbb-ccc">
     *     <a href="/logout" class="link_as_form">Link</a>
     * </form>
     */
    const nodes = document.getElementsByClassName('link_as_form');

    for (const node of nodes) {
        node.addEventListener('click', (e) => {
            e.preventDefault();
            console.log(e.target)
            e.target.parentNode.submit();
        });
    }
});
