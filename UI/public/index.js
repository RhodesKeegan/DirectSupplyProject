class Banner extends React.Component {
  constructor(props) {
    super(props);
  }

  reportQuestion(e) {
    if (e.key === 'Enter') {
      console.log('here');
    }
  }

  componentDidMount() {
    let el = document.querySelector('.greeting');
    el.classList.add('fade-in');
  }

  render() {
    return /*#__PURE__*/React.createElement("div", {
      className: 'banner'
    }, /*#__PURE__*/React.createElement("h1", {
      className: 'greeting'
    }, /*#__PURE__*/React.createElement("b", null, "Hello, I'm Dr. AMPS")), /*#__PURE__*/React.createElement("form", null, /*#__PURE__*/React.createElement("label", null, /*#__PURE__*/React.createElement("p", {
      className: 'input'
    }, /*#__PURE__*/React.createElement("b", null, "Ask me about PTACs:")), /*#__PURE__*/React.createElement("input", {
      className: 'inputBox',
      type: 'text',
      name: 'name',
      onKeyDown: this.reportQuestion.bind(this)
    }))));
  }

}
// Class: SE2840 - Menu Filter
// Web Application entry point - window.onload

/**
 * Window onload function - Creates the menuItem (unfiltered) array
 *     and renders the application
 */
window.onload = () => {
  banner = /*#__PURE__*/React.createElement(Banner, null);
  ReactDOM.render( /*#__PURE__*/React.createElement(Banner, null), document.getElementById('root'));
  banner.componentDidMount;
};
