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

  // Populates info for game from gameData
  populateGameData(data: any): void {
    this.resultData = data;
    this.coverImage = data.sample_cover.image ? data.sample_cover.image : this.coverImage;
    this.screenshotImage = data.sample_screenshots[0] ? data.sample_screenshots[0].image : this.screenshotImage;
    this.description = data.description.length > 2 ? this.formattedDescription(data.description) : this.description;
  }

  // Sets reasoning to value from rec engine and formats
  async setReasoning(data: any){
    let rec = data['reasoning'];
    let attString = "";
    this.reasoning = `The similarity level between the input game and ${data['title']} is ${rec['similarityLevel'].toLowerCase()}.<br/>`;
    attString = "<p>The following attribute(s) match the input game:</p><ul>";
    for(let att in rec['matchingAttributes']){
      attString = attString + `<li>${rec['matchingAttributes'][att]}</li>`;
    }
    this.reasoning = this.reasoning + attString;
  }
  
  // Format description from paragraph to a more readable state
  formattedDescription(description: any) {
    let sentences = description.split(". ");
    let formattedDescription = "";
    let breakCounter1 = 0;
    let breakCounter2 = 0;

    for(let i = 0; i < sentences.length; i++) {
      formattedDescription = formattedDescription + sentences[i] + ". ";
      breakCounter1 ++;
      if(breakCounter1 === 3) {
        formattedDescription = formattedDescription + "<br/>";
        breakCounter1 = 0;
        breakCounter2 ++;
      }
      if(breakCounter2 === 2){
        formattedDescription = formattedDescription + "<br/>";
        breakCounter2 = 0;
      }
    }
    return formattedDescription
  }
}
