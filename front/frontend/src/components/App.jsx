import React from 'react';
import axios from 'axios';
import { Route, Switch, Redirect } from 'react-router-dom';
import '../styles/App.css';

import Spinner from "react-bootstrap/Spinner";

import Login from "./Authentication/Login";

import Character from "./Character";
import Arena from "./Arena";
import Expedition from "./Expedition";

import Trader from "./NPC/Trader";
import Healer from "./NPC/Healer";

import Manage from "./Manage";
import Logout from "./Logout";

import Menu from "./Menu";
import NotLoggedInMenu from "./Authentication/NotLoggedInMenu";

import { REFRESH_PATH } from "../constants/routes";
import Ranking from "./Ranking";
import Register from "./Authentication/Register";

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isAuthenticated: false,
            isLoading: true,
            characterGold: 0,
            characterLevel: 1,
        }
    }

    componentDidMount() {
        this.sendGetRequest(REFRESH_PATH, true)
            .then((response) => {
                this.setIsAuthenticated(true);
                this.setState({isLoading: false});
                window.localStorage.setItem('access_token', response['data']['access_token']);
                window.localStorage.setItem('refresh_token', response['data']['refresh_token']);
            }).catch((error) => {
                this.setIsAuthenticated(false);
                this.setState({isLoading: false});
        });
    };

    setIsAuthenticated = (newAuthenticationStatus) => {
        this.setState({isAuthenticated: newAuthenticationStatus});
    };

    setCharacterGold = (gold) => {
        this.setState({characterGold: gold});
    };

    setCharacterLevel = (level) => {
        this.setState({characterLevel: level});
    };

    prepareHeaders = (refresh) => {
        return refresh
                ?
                { 'Authorization': 'Bearer ' + window.localStorage.getItem('refresh_token') }
                :
                { 'Authorization': 'Bearer ' + window.localStorage.getItem('access_token') };
    };

    sendGetRequest = (path, refresh=false) => {
        const headers = this.prepareHeaders(refresh);

        return new Promise((resolve, reject) => {
            axios.get(path, {
                headers: headers,
            }).then((response) => {
                resolve(response);
            }).catch((error) => {
                if (error.response.status === 401) {
                    this.setIsAuthenticated(false);
                }
                reject(error);
            })
        })
    };

    sendGetRequestWithData = (path, params) => {
        const headers = this.prepareHeaders(false);

        return new Promise((resolve, reject) => {
            axios.get(path, {
                params: params,
                headers: headers
            }).then((response) => {
                resolve(response);
            }).catch((error) => {
                if (error.response.status === 401) {
                    this.setIsAuthenticated(false);
                }
                reject(error);
            })
        })
    };

    sendPostRequest = (path, data, refresh=false) => {
        const headers = this.prepareHeaders(refresh);

        return new Promise((resolve, reject) => {
            axios.post(path, data,{
                headers: headers,
            }).then((response) => {
                resolve(response);
            }).catch((error) => {
                if (error.response.status === 401) {
                    this.setIsAuthenticated(false);
                }
                reject(error);
            })
        })
    };

    sendDeleteRequest = (path) => {
        const headers = this.prepareHeaders(false);

        return new Promise((resolve, reject) => {
            axios.delete(path, {headers: headers})
                .then((response) => {
                    resolve(response);
                }).catch((error) => {
                    console.log(error.response);
                    reject(error);
            })
        })
    };

    render() {

        if (this.state.isLoading) {
            return (
                <Spinner animation="primary" />
            );
        }

        return (
            <React.Fragment>
                {this.state.isAuthenticated
                ?
                    <Menu className="top-side-menu pb-0 mb-0"
                        sendPostRequest={this.sendPostRequest}
                        setIsAuthenticated={this.setIsAuthenticated}
                        characterGold={this.state.characterGold}
                        characterLevel={this.state.characterLevel}
                    />
                : <NotLoggedInMenu className="top-side-menu" />
                }
                <Switch>
                    <Route exact path="/">
                        {
                            this.state.isAuthenticated
                                ? <Redirect to="/login" />
                                : <Redirect to="/character" />
                        }
                    </Route>

                    <Route exact path="/login">
                        {
                            !this.state.isAuthenticated
                                ?
                                <Login setIsAuthenticated={this.setIsAuthenticated} />
                                : <Redirect to="/character" />
                        }
                    </Route>

                    <Route exact path="/register">
                        {
                            !this.state.isAuthenticated
                                ?
                                <Register setIsAuthenticated={this.setIsAuthenticated} />
                                : <Redirect to="/character" />
                        }
                    </Route>

                    <Route path="/character">
                        {
                            this.state.isAuthenticated
                                ?
                                <Character
                                    sendGetRequest={this.sendGetRequest}
                                    sendPostRequest={this.sendPostRequest}
                                    setCharacterGold={this.setCharacterGold}
                                    setCharacterLevel={this.setCharacterLevel}
                                />
                                : <Redirect to="/login" />
                        }
                    </Route>

                    <Route path="/arena">
                        {
                            this.state.isAuthenticated
                                ?
                                <Arena
                                    sendGetRequest={this.sendGetRequest}
                                    sendPostRequest={this.sendPostRequest}
                                />
                                : <Redirect to="/login" />
                        }
                    </Route>

                    <Route path="/expedition">
                        {
                            this.state.isAuthenticated
                                ?
                                <Expedition
                                    sendGetRequest={this.sendGetRequest}
                                    sendPostRequest={this.sendPostRequest}
                                    setCharacterGold={this.setCharacterGold}
                                    setCharacterLevel={this.setCharacterLevel}
                                />
                                : <Redirect to="/login" />
                        }
                    </Route>

                    <Route path="/npc/trader">
                        {
                            this.state.isAuthenticated
                                ?
                                <Trader
                                    sendGetRequest={this.sendGetRequest}
                                    sendPostRequest={this.sendPostRequest}
                                    setCharacterGold={this.setCharacterGold}
                                />
                                : <Redirect to="/login" />
                        }
                    </Route>

                    <Route path="/npc/healer">
                        {
                            this.state.isAuthenticated
                                ? <
                                Healer
                                    sendGetRequest={this.sendGetRequest}
                                    sendPostRequest={this.sendPostRequest}
                                    setCharacterGold={this.setCharacterGold}
                                />
                                : <Redirect to="/login" />
                        }
                    </Route>

                    <Route path="/ranking">
                        {
                           <
                            Ranking
                            sendGetRequestWithData={this.sendGetRequestWithData}
                            />
                        }
                    </Route>

                    <Route path="/manage">
                        {
                            this.state.isAuthenticated
                                ?
                                <Manage
                                    sendGetRequest={this.sendGetRequest}
                                    sendPostRequest={this.sendPostRequest}
                                    sendDeleteRequest={this.sendDeleteRequest}
                                    setIsAuthenticated={this.setIsAuthenticated}
                                />
                                : <Redirect to="/login" />
                        }
                    </Route>

                    <Route path="/logout">
                        {
                            this.state.isAuthenticated
                                ?
                                <Logout
                                    sendGetRequest={this.sendGetRequest}
                                    sendPostRequest={this.sendPostRequest}
                                />
                                : <Redirect to="/login" />
                        }
                    </Route>
                </Switch>
            </React.Fragment>
        )
    }
}

export default App;