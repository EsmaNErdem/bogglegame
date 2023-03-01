class Boggle {
   
    constructor(){
        this.secs = 60;
        this.showTimer();
        this.timer = setInterval(this.time.bind(this), 1000)
        this.score = 0;
        this.words = []
        $('#word-search').on("submit", this.handleSubmit.bind(this))
    }

    async time(){
        this.secs -= 1;
        this.showTimer(); 
        
        if(this.secs < 0){
            clearInterval(this.timer);
            $('#timer').text('TIME IS UP!');
            await this.finishGame()
        }      
    }

    showTimer(){
        $('#timer').text(`${this.secs} secs left`);
    }

    showScore(){
        $("#score").text(`Score: ${this.score}`);
    }
    
    showMsg(msg) {
        $('#msg').text(msg);
    }

    addWord(searchWord) {
        $('#words-list').append(`<li>${searchWord}</li>`);
        this.showMsg(`${searchWord} is added!`);
    }

    
    async handleSubmit(e) {
        e.preventDefault();
        let searchWord = $("#word").val();
        $('#word-search').trigger("reset");
        const result = await axios.get('/check-word',{params: {word: searchWord}});
        console.log()
        if (result.data.result == "not-word" ) {
            this.showMsg(`${searchWord} is not a word`);
        } else if (result.data.result == "not-on-board"){
            this.showMsg(`${searchWord} is not on the board`);
        } else {
            this.addWord(searchWord);
            this.words.push(searchWord);
            this.score += searchWord.length;
            this.showScore();
        }
        
        if(!searchWord) return
        if(this.words.includes(searchWord)){
            this.showMsg(`${searchWord} already exists`)
            return
        }
    }

    async finishGame() {
        $('#word-search').hide()
        $("#score").hide()
        const response = await axios.post("/finish-game", {score: this.score})
        if (response.data.high_score === this.score){
            this.showMsg(`${response.data.high_score} is the new highest score`)
        } else {
            this.showMsg(`Current score:${this.score} Highest Score remains as ${response.data.high_score}`)
        }
    }
}

