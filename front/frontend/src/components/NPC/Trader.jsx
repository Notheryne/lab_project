import React from 'react';
import '../../styles/Trader.css';
import Jumbotron from "react-bootstrap/Jumbotron";
import {ITEM_STAT_DISPLAY_NAME, TRADER_PATH, TRADER_TRADE_PATH} from "../../constants/routes";
import {Image} from "react-bootstrap";
import Spinner from "react-bootstrap/Spinner";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import Tooltip from "react-bootstrap/Tooltip";

class Trader extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoading: true,
            itemsReady: false,
            npcName: '',
            npcImagePath: '',
            npcText: '',
            charGold: 0,
            traderItems: {},
        }
    }


    componentDidMount() {
        this.props.sendGetRequest(TRADER_PATH)
            .then((response) => {
                this.setState({npcName: response['data']['name']});
                this.setState({npcImagePath: response['data']['img_path']});
                this.setState({npcText: response['data']['text']});
                this.setState({charGold: response['data']['gold']});
                this.props.setCharacterGold(response['data']['gold']);
                this.setState({traderItems: response['data']['items']});
                this.setState({isLoading: false});
            }).catch((error) => {
                console.log(error.response);
        })
    }

    getItemDescription = (itemData) => {
        const stats = Object.keys(ITEM_STAT_DISPLAY_NAME).map(statName => {
            return (
                <p key={statName} className="item-description-row">{ITEM_STAT_DISPLAY_NAME[statName]}: {itemData[statName]}</p>
            );
        });
        return (
            <Tooltip id="tooltip-bottom">
                <strong>{itemData['name']}</strong> <br/>
                <small>{itemData['slot']}</small> <br/>
                <strong>Price: {itemData['price']}</strong>
                {stats}
            </Tooltip>
        );
    };

    buyItem = (itemId) => {
        this.props.sendPostRequest(TRADER_TRADE_PATH, {bp_id: itemId})
            .then((response) => {
                this.props.setCharacterGold(response['data']['gold']);
            }).catch((error) => {
                console.log(error.response);
        })
    };

    renderItemsRow = (itemsInRow) => {
        const items = itemsInRow.map((itemData) => {
            const itemName = itemData['name'];
            const itemId = itemData['id'];

            return (
                <Col
                    key={"item-data-for-" + itemName + "-(id " + itemId + ")"}
                    xs="auto"
                    className="m-auto trader-column"
                    // style={{border: "2px groove rgba(12, 7, 15, 0.3)",}}
                >
                    <OverlayTrigger
                        trigger="hover"
                        placement="bottom"
                        overlay={this.getItemDescription(itemData)}
                    >
                        <Image
                            src={itemData['img_path']}
                            className="d-inline-block p-2"
                            height={220}
                            width={140}
                            onClick={() => {this.buyItem(itemId)}}
                        />
                    </OverlayTrigger>
                    <p
                        className="bg-dark text-light trader-item-name"
                        style={{width: 140, whiteSpace: "nowrap"}}
                    >
                        <strong>{itemData['name']}</strong>
                    </p>
                </Col>
            )
        });
        return items;
    };

    renderItems = () => {
        const topRowItems = this.state.traderItems.slice(0, 3);
        const bottomRowItems = this.state.traderItems.slice(3, 6);
        const topRow = this.renderItemsRow(topRowItems);
        const bottomRow = this.renderItemsRow(bottomRowItems);
        const rowClassName = "bg-light w-75 m-auto";
        return (
            <React.Fragment>
                <Row className={rowClassName}>
                    {topRow}
                </Row>
                <Row className={rowClassName}>
                    {bottomRow}
                </Row>
            </React.Fragment>
        )
    };

    render() {
        if (!this.state.isLoading) {
            return (
                <Jumbotron>
                    <div className="text-center">
                        <Image
                            src={this.state.npcImagePath}
                            height={300}
                            width={280}
                            alt="healer image"
                        />
                        <span className="mt-3 form-control">
                            <strong>{this.state.npcName}</strong>: {this.state.npcText}
                        </span>
                    </div>
                    <div className="mt-3">
                        {this.renderItems()}
                    </div>
                </Jumbotron>
            );
        } else {
            return (
                <Spinner animation="primary"/>
            );
        }
    }
}

export default Trader;