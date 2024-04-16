import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { GenerateComponent } from './generate/generate.component';
import { ResultsComponent } from './results/results.component';
import { NavigationComponent } from './navigation/navigation.component';
import { UserpageComponent } from './userpage/userpage.component';
import { AuthModule } from '@auth0/auth0-angular';
import { HttpClientModule } from '@angular/common/http';
import { NgSelectModule } from '@ng-select/ng-select';
import { FormsModule } from '@angular/forms';
import { HistoryComponent } from './history/history.component';
import { LibraryComponent } from './library/library.component';


@NgModule({
  declarations: [
    AppComponent,
    GenerateComponent,
    ResultsComponent,
    NavigationComponent,
    UserpageComponent,
    HistoryComponent,
    LibraryComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    HttpClientModule,
    AuthModule.forRoot({
      domain: 'dev-x4savaa1u24lh134.us.auth0.com',
      clientId: 'ANr89J95cdCL9E2XhqoeBkA4TqLwO0hI',
      authorizationParams: {
      redirect_uri: window.location.origin
    }}),
    NgSelectModule, 
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
