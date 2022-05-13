

const file_id = 'file-aIg2j8DE38wMQKX3pxu2CJTU'
const example_context = "This appliance is not intended for use by persons (including children) with "+
    "reduced physical, sensory or mental capabilities, or lack of experience and "+
    "knowledge, unless they have been given supervision or instruction concerning use of the " +
    "appliance by a person responsible for their safety. Children should be supervised to ensure "+
    "they do not play with the appliance. "

const ex = [["Who can operate the PTAC?","Persons (including children) with reduced physical, sensory, or mental capabilities, or lack of experience and knowledge can operate the PTAC, provided they have been given supervision or instruction by a person responsible for their safety."], ["Can children play with the PTAC?", "Children should be supervised to ensure they do not play with the appliance."]]


async function askQuestion(e){
    if(e.key === 'Enter'){
        const url = "https://api.openai.com/v1/answers";
        const question = e.target.value
        const xhr = new XMLHttpRequest();
        xhr.open("POST", url);

        xhr.setRequestHeader("Authorization", "Bearer ***REMOVED***");
        xhr.setRequestHeader("Content-Type", "application/json");

        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                const responseArea = document.getElementById('responseArea');
                responseArea.style.display = 'block';
                let response = JSON.parse(xhr.responseText)


                response = response.answers[0].replace(/=-/g, '')

                responseArea.innerText = response

                var speechVoice = new SpeechSynthesisUtterance();
                var voices = speechSynthesis.getVoices();
                speechVoice.voice = voices[2];
                speechVoice.text = response
                speechVoice.lang = 'en-GB';
                speechSynthesis.speak(speechVoice);
            }};

        const data = `{
    "file": "${file_id}",
    "question": "${question}",
    "search_model": "ada",
    "model": "curie",
    "examples_context": "${example_context}",
    "examples": [["Who can operate the PTAC?","Persons (including children) with reduced physical, sensory, or mental capabilities, or lack of experience and knowledge can operate the PTAC, provided they have been given supervision or instruction by a person responsible for their safety."], ["Can children play with the PTAC?", "Children should be supervised to ensure they do not play with the appliance."]],
    "max_tokens": 50
  }`;

        xhr.send(data)
    }
}

class Banner extends React.Component {
    constructor(props) {
        super(props);
        this.cursor_ref = React.createRef()
        this.cursor = <span ref={this.cursor_ref}>_</span>;
        this.display = true;
    }

    state_change(){
        setInterval(()=>{
            if(this.display){
                this.cursor_ref.current.style.opacity = 0;
                this.display = false;
            }else{
                this.cursor_ref.current.style.opacity = 1;
                this.display = true;
            }
        }, 500)
    }

    componentDidMount() {
        this.state_change()
    }

    render() {
        return(
            <div>
                <div className={'banner'}>
                    <h1 className={'greeting fade-in-greeting'}><b>Hello, I'm Dr. AMPS</b>{this.cursor}</h1>
                    <form onSubmit={(e)=>{e.preventDefault()}}>
                        <label>
                            <p className={'input fade-in-subtext'}>
                                <b>Ask me about PTACs:</b>
                            </p>
                            <input className={'inputBox'} type={'text'} name={'name'} onKeyDown={askQuestion.bind(this)}/>
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
