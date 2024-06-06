import React, {useState} from 'react';
import axios from 'axios';
import './RecipeGenerator.css';

const RecipeGenerator = () => {

    const [recipe, setRecipe] = useState('');

    const handleGenerateRecipe = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch('http://localhost:5000/generate_recipe', {
                method: 'POST',
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(body)
            });
            const recipeData = response.data.recipe;
            setRecipe(recipeData);
        } catch (error){
            console.error('Error generating recipe', error);
        }

    };

    const [additionalComments, setComments] = useState('');

    return(
        <div className="comments-container">
            <input type="text" className="comments-input" value={additionalComments} placeholder='additional comments' onChange={(e) => {
                setComments(e.target.value)
            }}/>
            <button className="comments-submit">Submit</button>
        </div>
    );
};

export default RecipeGenerator;