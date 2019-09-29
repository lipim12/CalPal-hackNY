import React from 'react';

type TotalCaloriesProps = {
    calories: string | null;
}

type TotalCaloriesDefaultProps = {
    calories: string | null;
}

export default class TotalCalories extends React.Component<TotalCaloriesDefaultProps, TotalCaloriesProps, void>{ 
    static defaultProps = {
        calories: '2000',
    };

  static displayName = 'TotalCalories';
  render(){
      const calories = this.props.calories;
      return (
        <div>
           You set your daily calories intake to: {calories} kCal;
           <p style={{ fontSize: '0.5em'}}>All the suggested values are based on one standard portion</p>
        </div>
  );
  }
}

