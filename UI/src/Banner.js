

class Banner extends React.Component {
    constructor(props) {
        super(props);
    }

    reportQuestion(e){

        if(e.key === 'Enter'){
            let question = e.target.value;
            //DO STUFF HERE FOR ADDING ACTUAL RESPONSE
            const responseArea = document.getElementById('responseArea');
            responseArea.style.display = 'block';
        }
    }

    componentDidMount(){
        let el = document.querySelector('.greeting');
        el.classList.add('fade-in');
    }

    render() {
        return(
            <div>
                <div className={'banner'}>
                    <h1 className={'greeting fade-in-greeting'}><b>Hello, I'm Dr. AMPS</b></h1>
                    <form onSubmit={(e)=>{e.preventDefault()}}>
                        <label>
                            <p className={'input fade-in-subtext'}>
                                <b>Ask me about PTACs:</b>
                            </p>
                            <input className={'inputBox'} type={'text'} name={'name'} onKeyDown={this.reportQuestion.bind(this)}/>
                        </label>
                    </form>
                    <div>
                        <p id={'responseArea'}>Response Goes Here</p>
                    </div>
                </div>
            </div>

        )
    }

}
