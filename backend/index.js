const express = require("express");
const app = express();
const Pool = require("pg").Pool;
const cors = require("cors")
const { Configuration, OpenAI } = require("openai");


const openai = new OpenAI({apiKey:""})

const pool = new Pool({
    user: "postgres",
    password: "",
    host: "localhost",
    port: 5432,
    database: "fridgepal"
});

//const openai = new OpenAI('')

//middleware
app.use(cors());
app.use(express.json());

//ROUTES

//create labels
app.post("/labels", async (req, res) => {
    try {
        const { description } = req.body;
        const newLabel = await pool.query("INSERT INTO labels (description) VALUES($1) RETURNING *", [description])  

        res.json(newLabel.rows[0])
    } catch (error) {
        console.error(error.message)
        
    }
});

//get labels
app.get("/labels", async (req, res) => {
    try {
        const allLabels = await pool.query("SELECT * FROM labels")
        res.json(allLabels.rows)

    } catch (error) {
        console.error(error.message)
    }
});

//generate recipe
app.post("/generate_recipe", async (req, res) => {
    try {
        const getLabels = await pool.query("SELECT * FROM labels")
        const labels = getLabels.rows
        const { allergies, mealType, calories, comments } = req.body

        let prompt= 'Create a new recipe using only the following ingredients (you do not have to use ALL of them, but you cannot use anything that is not listed):\n'
        labels.forEach((label) => {
            prompt += `- ${label.description}\n`;
        })
        prompt += `\nPreferences:\n`;
        prompt += `Allergies: ${allergies}\n`;
        prompt += `Meal Type: ${mealType}\n`;
        prompt += `Calories: ${calories}\n`;
        prompt += `Calories: ${comments}\n`;

        response = await openai.chat.completions.create({
            model: "gpt-3.5-turbo",
            messages: [{"role": "system", "content": "You are a helpful assistant that generates recipes."}, {"role": "user", "content": prompt}]
        })
        const recipe = response.choices[0].message.content.trim();
        console.log(recipe)

        res.json({recipe})

    } catch (error) {
        console.error(error.message)
    }
})



app.listen(5000, () => {
    console.log('server has started')
})
