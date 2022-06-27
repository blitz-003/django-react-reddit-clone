import {
    createAsyncThunk,
    createEntityAdapter,
    createSlice,
} from "@reduxjs/toolkit";

const API_ENDPOINT = process.env.REACT_APP_API_ENDPOINT;

const categoriesAdapter = createEntityAdapter();

const initialState = categoriesAdapter.getInitialState({
    status: "idle",
    error: null,
});

export const fetchCategories = createAsyncThunk(
    "categories/fetchCategories",
    async () => {
        const response = await fetch(`${API_ENDPOINT}/categories/`);
        if (!response.ok) {
            return Promise.reject(response.status);
        }
        const json = await response.json();
        return json;
    }
);

export const createCategory = createAsyncThunk(
    "categories/createCategory",
    async (newCategory) => {
        const response = await fetch(`${API_ENDPOINT}/categories/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            body: JSON.stringify(newCategory),
        });
        if (!response.ok) {
            Promise.reject(response.status);
        }
        const json = await response.json();
        return json;
    }
)

const categoriesSlice = createSlice({
    name: "categories",
    initialState,
    reducers: {},
    extraReducers(builder) {
        builder
            .addCase(fetchCategories.pending, (state, action) => {
                state.status = "pending";
            })
            .addCase(fetchCategories.fulfilled, (state, action) => {
                state.status = "fulfilled";
                categoriesAdapter.setAll(state, action.payload);
            })
            .addCase(fetchCategories.rejected, (state, action) => {
                state.status = "rejected";
                state.error = action.error.message;
            })
            .addCase(createCategory.fulfilled, (state, action) => {
                categoriesAdapter.addOne(state, action.payload);
            })
    },
});

export default categoriesSlice.reducer;

export const {
    selectAll: selectAllCategories,
    selectById: selectCategoryById,
    selectIds: selectCategoryIds,
} = categoriesAdapter.getSelectors((state) => state.categories);
