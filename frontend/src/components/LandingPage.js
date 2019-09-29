import React from 'react';
import Col from 'react-bootstrap/lib/Col';
import Dropdown from 'react-bootstrap/lib/Dropdown';
import Row from 'react-bootstrap/lib/Row';
import { AxiosProvider, Request, Get, Delete, Head, Post, Put, Patch, withAxios } from 'react-axios';

import FileBase64 from './FileBase64.js';
import TotalCalories from './TotalCalories.js';

type LandingPageProps = {
  error:string;
  response: string;
  isLoading: string;
  makeRequest: string;
  axios: string;
};

type LandingPageState = {
  pictures: Array<any>;
};

export default class LandingPage extends React.Component<void, LandingPageProps, LandingPageState> {

    constructor(props) {
        super(props);
         this.state = { pictures: [] };
         (this:any).getFiles = this.getFiles.bind(this);
         (this:any).postReq = this.postReq.bind(this);
    }

    static displayName = 'LandingPage';

    shouldComponentUpdate(nextState){
        if(this.state.pictures!==nextState.pictures){
            return true;
        }
    }

    
    postReq(img: string){
        const MyComponent = withAxios({url: 'http://10.16.77.148:5000/add', params: { "image": img}})
        (class MyComponentRaw extends React.Component {
            render() {
                const {error, response, isLoading, makeRequest, axios} = this.props
                if(error) {
                return (<div>Something bad happened: {error.message}</div>)
                } else if(isLoading) {
                return (<div className="loader"></div>)
                } else if(response !== null) {
                return (<div>{response.data.message}</div>)
                }
                return null
            }
        })
    }

    getFiles(files){
        this.setState({ 
            pictures: files,
        },()=>{
            this.postReq(this.state.pictures.base64.substr(23));
        });
        console.log(this.state.pictures.base64.substr(23));
    }
    
    render() {
        const previewComp = this.state.pictures.length > 0 ? 
            (<img src={this.state.pictures.fileURL} alt="" id="show-picture" style={{ height: '100px' }} />) 
            : '';
        
        const food = ['grapes','melon','watermelon','tangerine','lemon','banana','pineapple','red apple','green apple','pear','peach','cherries','strawberry','kiwifruit','tomato','avocado','eggplant','potato','carrot','corn','hot pepper','cucumber','mushroom','peanuts','chestnut','bread','croissant','french bread','pancakes','cheese','beef','chicken','bacon','hamburger','french fries',
                        'pizza','hotdog','taco','burrito','popcorn','rice crackers','rice','spaghetti','fried shrimp','icecream','doughnut','cookie','cake','chocolate bar','candy','custard flan','honey','milk','black tea','sake','champagne','red wine','beer'];
        return (
            <Col xs={12} sm={12} md={12} lg={12} style={{ textAlign: 'center', fontFamily:'montserrat', fontWeight: '100', color:'white' }}>
                <Row>
                    <h3>Feeling hungry again? 
                    <br/>
                    Let's see how many calories are you eating.</h3>
                    <br />
                    <TotalCalories/>
                    
                    <br/>
                    <span style={{ fontWeight: '400' }}>
                        Take a <img src={require('../resources/camera_emoji.png')} alt="" style={{ height: '30px', width: 'auto' }} /> of your food <img src={require('../resources/burger_emoji.png')} alt="" style={{ height: '30px', width: 'auto' }} />
                    </span>
                    <br/>
                    OR
                    <br/>
                </Row>
                
                <Row>
                    
                    <FileBase64
                        multiple={ false }
                        onDone={ this.getFiles } />
                </Row>
                <Row>
                    <br/>
                    <img src={this.state.pictures.fileURL} alt="" id="show-picture" style={{ height: '100px' }} />
                    {/* <Post url='http://10.16.77.148:5000/add' params={{"image": this.state.pictures.base64.substr(23)}}>
        {(error, response, isLoading, makeRequest, axios) => {
          if(error) {
            return (<div></div>)
          }
          else if(isLoading) {
            return (<div>Loading...</div>)
          }
          else if(response !== null) {
            return (<div>{response.data.message} <button onClick={() => makeRequest({ params: { refresh: true } })}>Refresh</button></div>)
          }
          return (<div>Default message before request is made.</div>)
        }}
      </Post> */}
                </Row>
            </Col>
            
        );
    }
}