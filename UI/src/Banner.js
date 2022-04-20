

class Banner extends React.Component {
    constructor(props) {
        super(props);
    }

    reportQuestion(e){
        if(e.key === 'Enter'){
            console.log('here')
        }
    }

    componentDidMount(){
        let el = document.querySelector('.greeting');
        el.classList.add('fade-in');
    }

    render() {
        return(
            <div className={'banner'}>
                <h1 className={'greeting'}><b>Hello, I'm Dr. AMPS</b></h1>
                <form>
                    <label>
                        <p className={'input'}>
                            <b>Ask me about PTACs:</b>
                        </p>
                        <input className={'inputBox'} type={'text'} name={'name'} onKeyDown={this.reportQuestion.bind(this)}/>
                    </label>
                </form>
            </div>

        )
    }

}
