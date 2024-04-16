import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiserviceService {

  apiUrl = 'http://127.0.0.1:5000';

  constructor(private http: HttpClient) { }

  getGames(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/api/v1.0/games`);
  }

  getGameRec(id: number, useSentiment:boolean, useLibrary:boolean, userId?:string, ): Observable<any> {
    if(userId) {
      return this.http.get<any[]>(`${this.apiUrl}/api/v1.0/games/rec/${id}?useSentiment=${useSentiment}&useLibrary=${useLibrary}&userId=${userId}`);
    }
    return this.http.get<any[]>(`${this.apiUrl}/api/v1.0/games/rec/${id}?useSentiment=${useSentiment}&useLibrary=${useLibrary}`);
  }

  getGameById(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/v1.0/games/${id}/info`);
  }

  searchGames(term: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/v1.0/games/search/${term}`);
  }

  addUser(userData: any): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/api/v1.0/users`, userData);
  }

  getUserHistory(id: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/v1.0/users/${id}/history`);
  }

  setUserHistory(id: string, data: any): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/api/v1.0/users/${id}/history`, data);
  }

  getUserLibrary(id: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/v1.0/users/${id}/library`);
  }

  setUserLibrary(id: string, data: any): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/api/v1.0/users/${id}/library`, data);
  }

  deleteFromLibrary(id: string, lid: string): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/api/v1.0/users/${id}/library/delete/${lid}`);
  }

  deactivateUser(id: string): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/api/v1.0/users/${id}/deactivate`);
  }

  clearUserHistory(id: string): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/api/v1.0/users/${id}/history/clear`);
  }

  clearUserLibrary(id: string): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/api/v1.0/users/${id}/library/clear`);
  }

  addSuggestion(suggestion: any): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/api/v1.0/suggestions`, suggestion);
  }
}
