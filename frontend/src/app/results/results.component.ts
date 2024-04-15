import { Attribute, Component } from '@angular/core';
import { ApiserviceService } from '../apiservice.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrl: './results.component.css'
})
export class ResultsComponent {
  constructor(
    private api: ApiserviceService,
    private route: ActivatedRoute,
    private router: Router
  ) {}
  
  resultData: any = [];
  data: any;
  coverImage: string = "../assets/img/No_image_available.png";
  screenshotImage: string = "";
  description: string = "No description available.";
  reasoning: string = "No reasoning available.";

  async ngOnInit() {
    this.api.getGameById(this.route.snapshot.params['id']).subscribe(data => this.populateGameData(data));
    await this.setReasoning(history.state);
  }

  populateGameData(data: any): void {
    this.resultData = data;
    this.coverImage = data.sample_cover.image ? data.sample_cover.image : this.coverImage;
    this.screenshotImage = data.sample_screenshots[0] ? data.sample_screenshots[0].image : this.screenshotImage;
    this.description = data.description.length > 2 ? this.formatDesc(data.description) : this.description;
  }

  async setReasoning(data: any){
    let rec = data['reasoning'];
    let attString = "";
    this.reasoning = `The similarity level between the input game and ${data['title']} is ${rec['similarityLevel'].toLowerCase()}.<br/>`;
    attString = "<p>The following attribute(s) match the input game:</p><ul>";
    console.log(rec['matchingAttributes']);
    for(let att in rec['matchingAttributes']){
      attString = attString + `<li>${rec['matchingAttributes'][att]}</li>`;
    }
    this.reasoning = this.reasoning + attString;
  }
  
  // Formats description into a more readable state
  // TODO make this less plagiarismy/clean it up
  formatDesc(description: any) {
    let sentenceArr = description.split(". ");
    let formatDesc = "";
    let counter = 0;
    let counter2 = 0;

    for(let i = 0; i < sentenceArr.length; i++) {
      formatDesc = formatDesc + sentenceArr[i] + ". ";
      counter ++;
      if(counter === 3) {
        formatDesc = formatDesc + "<br/>";
        counter = 0;
        counter2 ++;
      }
      if(counter2 === 2){
        formatDesc = formatDesc + "<br/>";
        counter2 = 0;
      }
    }
    return formatDesc
  }
}
