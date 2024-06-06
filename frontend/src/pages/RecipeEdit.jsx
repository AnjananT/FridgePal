import React, { useState } from 'react'
import axios from 'axios';
import './RecipeEdit.css';
import '../components/RecipeGenerator.css'
import Select from 'react-select';

const options = [
    {value: 'breakfast', label: 'Breakfast'},
    {value: 'lunch', label: 'Lunch'},
    {value: 'dinner', label: 'Dinner'}

];


const RecipeEdit = ({ onSubmit }) => {
    const [selectedAllergies, setSelectedAllergies] = useState([]);
    const [selectedMealType, setSelectedMealType] = useState(' ');
    const [calories, setCalories] = useState(0);
    const[recipe, setRecipe] = useState('');
    const [additionalComments, setComments] = useState('');
    
    const handleSubmit = async (event) => {
        event.preventDefault();
        
        const body = {
            allergies: selectedAllergies,
            mealType: selectedMealType,
            calories: calories,
            comments: additionalComments
        }

        try {
            const response = await fetch('http://localhost:5000/generate_recipe', {
                method: 'POST',
                headers: { "Content-Type": "application/json"},
                body: JSON.stringify(body)
            });
            const jsonData = await response.json()
            setRecipe(jsonData.recipe)
            console.log('Recipe generated:', jsonData.recipe);
            // Handle the generated recipe as needed
        } catch (error) {
            console.error('Error generating recipe:', error);
        }
    };

    const handleAllergyChange = (event) => {
        const { value, checked } = event.target;
        if (checked) {
            setSelectedAllergies(prevAllergies => [...prevAllergies, value]);
        } else {
            setSelectedAllergies(prevAllergies => prevAllergies.filter(allergy => allergy !== value));
        }
    };

    const customStyles = {
        control: (base, state) => ({
        ...base,
        background: "#7BA4D3",
        fontSize: 15,
        height: 0,
        minHeight: 28,
    
        }),
        menu: base => ({
        ...base, 
        background: "#7BA4D3",
        fontSize: 13,
        }),

        dropdownIndicator: (base) => ({
        ...base,
        minHeight: 1,
        height: 0,
        width: 20,
        minWidth: 0,
        color: "transparent",

        })
  
    };
    const handleMealType = (event) => {
        const { value, checked } = event.target;
        if (checked) {
            setSelectedMealType(prevMealType => [...prevMealType, value]);
        } else {
            setSelectedMealType(prevMealType => prevMealType.filter(mealType => mealType !== value));
        }
    };
    
    const handleCaloriesChange = (event) => {
        setCalories(event.target.value);
    };
    return (
        <div className = "container">
            <form onSubmit = {handleSubmit}>
                <div className = "left-side" >
                <h2> Preferences </h2>
                    <div className = "preferences-box">
                        <div className = "preferences-section">
                            <h2 className = "pref-title">Allergies</h2>
                            <label className = "checkboxEdit">
                                <input 
                                    type= "checkbox"
                                    value="gluten"
                                    onChange={handleAllergyChange}
                                    /> Gluten
                            </label>
                            <label className = "checkboxEdit">
                                <input
                                    type= "checkbox"
                                    value="dairy"
                                    onChange={handleAllergyChange}
                                    /> Dairy 
                            </label>
                            <label className = "checkboxEdit">
                                <input
                                    type= "checkbox"
                                    value="nuts"
                                    onChange={handleAllergyChange}
                                    /> Nuts
                            </label>
                            <label className = "checkboxEdit">
                                <input
                                    type= "checkbox"
                                    value="soy"
                                    onChange={handleAllergyChange}
                                    /> Soy
                            </label>
                            </div>
                        <div className="preferences-section">
                            <h2 className = "pref-title"> Meal Type</h2>
                            <label className = "checkboxEdit">
                                <input 
                                    type= "checkbox"
                                    value="gluten"
                                    onChange={handleMealType}
                                    /> Breakfast
                            </label>
                            <label className = "checkboxEdit">
                                <input
                                    type= "checkbox"
                                    value="dairy"
                                    onChange={handleMealType}
                                    /> Lunch 
                            </label>
                            <label className = "checkboxEdit">
                                <input
                                    type= "checkbox"
                                    value="nuts"
                                    onChange={handleMealType}
                                    /> Dinner
                            </label>
                        </div>
                        <div className="preferences-section">
                            <h2 className = "pref-title"> Calories:</h2>
                            <input
                                type="range"
                                min="0"
                                max="1000"
                                value={calories}
                                onChange={handleCaloriesChange}
                            />
                            <span>{calories}</span>
                        </div> 
                    </div> 
                    <div className="comments-container">
                    <input type="text" className="comments-input" value={additionalComments} placeholder='additional comments' onChange={(e) => {
                        setComments(e.target.value)
                    }}/>
                    <button className="comments-submit">Submit</button>
                </div>
                </div>
                
            </form>
            <div className = "right-side">
                <h2> Generated Recipe </h2>
                <div className = "recipe-box">
                <p className = "recipe-text">{recipe}</p>
                </div>
            </div>
        </div>
    );
}
export default RecipeEdit