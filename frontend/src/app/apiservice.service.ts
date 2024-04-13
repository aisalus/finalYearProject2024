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

  getGameRec(id: number): Observable<any> {
    return this.http.get<any[]>(`${this.apiUrl}/api/v1.0/games/rec/${id}`);
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

  getUserHistory(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/v1.0/users/${id}/history`);
  }

  setUserHistory(id: number, data: any): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/api/v1.0/users/${id}/history`, data);
  }

  getUserLibrary(id: number, post: any): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/v1.0/users/${id}/library`);
  }

  setUserLibrary(id: number, data: any): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/api/v1.0/users/${id}/library`, data);
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
}
