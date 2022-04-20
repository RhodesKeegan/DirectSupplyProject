// Class: SE2840 - Menu Filter
// Web Application entry point - window.onload

/**
 * Window onload function - Creates the menuItem (unfiltered) array
 *     and renders the application
 */
window.onload = () => {
    banner = <Banner/>
    ReactDOM.render(<Banner/>, document.getElementById('root'));
    banner.componentDidMount
}
