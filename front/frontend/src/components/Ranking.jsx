import React, {Component} from 'react';
import {RANKING_HEADERS_DISPLAY, RANKING_PATH} from "../constants/routes";
import Spinner from "react-bootstrap/Spinner";
import Table from "react-bootstrap/Table";
import Pagination from "react-bootstrap/Pagination";

class Ranking extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoading: true,
            activePage: 1,
            lastPage: -1,
            characters: {},
            price: 0,
            sortBy: 'experience',
            order: true,
            errorStatus: '',
        }
    }

    getRankingData = (header, order, activePage) => {
        const params = {
            'sort_by': header,
            'page': activePage,
            'price': this.state.price,
            'order': order ? 'desc' : 'asc',
        };
        this.props.sendGetRequestWithData(RANKING_PATH, params)
            .then((response) => {
                this.setState({characters: response['data']['characters']});
                this.setState({lastPage: response['data']['last_page']});
                this.setState({isLoading: false})
            }).catch((error) => {
            console.log(error.response);
            this.setState({errorStatus: error.response['data']['message']});
        })
    };

    componentDidMount() {
        this.getRankingData(this.state.sortBy, this.state.order, this.state.activePage);
    }

    handleTableHeaderClick = (header) => {
        this.setState({isLoading: true});
        let order;
        if (this.state.sortBy !== header) {
            this.setState({sortBy: header});
            order = this.state.order;
        } else {
            order = !this.state.order;
        }
        this.setState({order: order});
        this.getRankingData(header, order, this.state.activePage);
    };

    renderTableHead = () => {
        const headers = Object.keys(RANKING_HEADERS_DISPLAY).map(header => {
            return (
                <th onClick={() => this.handleTableHeaderClick(header)} key={header}>
                    {RANKING_HEADERS_DISPLAY[header]}
                </th>
            )});
        return (
            <React.Fragment>
                <th onClick={() => {this.handleTableHeaderClick('experience')}}>#</th>
                <th>Character Name</th>
                {headers}
            </React.Fragment>
        )};

    renderTableRows = () => {
        const characters = this.state.characters;
        return Object.keys(this.state.characters).map(characterNumber => {
            const characterData = characters[characterNumber];
            const stats = Object.keys(characterData).map(characterStat => {
                return <td key={characterData['name'] + '-' + characterStat}>{characterData[characterStat]}</td>
            });
            return (
                <tr key={characterNumber}>
                    <td>{characterNumber}</td>
                    {stats}
                </tr>
            )
        })
    };

    handlePageChange = (pageNumber) => {
        this.setState({activePage: pageNumber});
        this.getRankingData(this.state.sortBy, this.state.order, pageNumber);
    };

    getPages = () => {
        let pages = [];
        for (let number = 1; number <= this.state.lastPage; number++) {
            pages.push(
                <Pagination.Item value={number}
                                 key={number}
                                 active={number === this.state.activePage}
                                 onClick={() => this.handlePageChange(number)}>
                    {number}
                </Pagination.Item>
            )
        }
        return pages;
    };

    render() {
        if (!this.state.isLoading) {
            return (
                <React.Fragment>
                <div className="w-75 m-auto" style={{overflow: 'hidden'}}>
                    <Pagination className="float-right flex-nowrap">
                        {this.getPages()}
                    </Pagination>
                </div>
                <Table bordered hover striped className="w-75 ml-auto mr-auto text-center">
                    <thead>
                        <tr>
                            {this.renderTableHead()}
                        </tr>
                    </thead>
                    <tbody>
                        {this.renderTableRows()}
                    </tbody>
                </Table>
                </React.Fragment>
            );
        } else {
            return <Spinner animation="primary" />
        }
    }
}

export default Ranking;