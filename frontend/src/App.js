import React, { useState, useRef, useEffect, useMemo } from "react";
import styles from "./app.module.css"
import { AutoComplete } from 'primereact/autocomplete';
import { GrCaretNext, GrChapterNext, GrCaretPrevious, GrChapterPrevious } from "react-icons/gr";


function App() {
	const API_URL = "http://127.0.0.1:8080";
	useEffect(() => {
		const urlParams = new URLSearchParams(window.location.search);
		const queryParam = urlParams.get('query');
		const pageParam = urlParams.get('page');
		if (pageParam) {
			try {
				const queryPage = parseInt(pageParam);
				setCurrentPage(Math.max(1, queryPage));
			} catch (error) {
			}
		}
		if (queryParam) {
			setQuery(queryParam);
			fetchSearchResults(queryParam, pageParam || 1);
		}
	}, []);
	const [searchResults, setSearchResults] = useState(null);
	const [currentPage, setCurrentPage] = useState(1);
	const [autocomplete, setAutocomplete] = useState([]);
	const [query, setQuery] = useState("");
	const [loading, setLoading] = useState(false);
	const autoCompleteRef = useRef(null);


	async function handleSearch(event) {
		event.preventDefault();
		const url = new URL(window.location.href);
		url.searchParams.set('query', query);
		url.searchParams.set('page', 1);
		setCurrentPage(1);
		window.history?.pushState?.(null, '', url.toString());
		fetchSearchResults(query, 1);
	}

	async function fetchSearchResults(search_query, search_page) {
		try {
			if (!search_query) {
				search_query = query;
			}
			if (!search_page) {
				search_page = currentPage;
			}
			setLoading(true);
			const response = await fetch(`${API_URL}/api/search?query=${search_query}&page=${search_page}`);
			if (!response.ok) {
				throw new Error("Failed to fetch search results");
			}
			const data = await response.json();
			setSearchResults(data);
			setTimeout(() => {
				setLoading(false);
			}, 500);

		}
		catch (error) {
			console.error(error);
		}
	}

	async function handleChange(event) {
		const value = event.target.value;
		setQuery(value);
		fetchAutocomplete(value, currentPage);
	}

	async function fetchAutocomplete() {
		if (autoCompleteRef.current) {
			autoCompleteRef.current.abort();
		}
		if (query === "") {
			setAutocomplete([]);
			return;
		}
		const controller = new AbortController();
		autoCompleteRef.current = controller;
		const signal = controller.signal;
		try {
			const response = await fetch(`${API_URL}/api/autocomplete?query=${query}`, { signal });
			if (!response.ok) {
				throw new Error("Failed to fetch autocomplete");
			}
			const data = await response.json();
			setAutocomplete(data);
		} catch (error) {
			console.error(error);
		}

	}

	async function handlePageChange(page) {
		setCurrentPage(page);
		const url = new URL(window.location.href);
		url.searchParams.set('page', page);
		window.history?.pushState?.(null, '', url.toString());
		fetchSearchResults(query, page);
	}

	const start = (currentPage - 1) * 10 + 1;

	function handleComplete(event) {
		const value = event.value;
		const words = query.split(" ");
		words[words.length - 1] = value;
		setQuery(words.join(" "));
	}

	function handleDidYouMean() {
		const url = new URL(window.location.href);
		url.searchParams.set('query', searchResults.did_you_mean);
		url.searchParams.set('page', 1);
		setQuery(searchResults.did_you_mean);
		setCurrentPage(1);
		window.history?.pushState?.(null, '', url.toString());
		fetchSearchResults(searchResults.did_you_mean, 1);
	
	}

	return (
		<div className={styles.app}>
			<form className={styles.form} onSubmit={handleSearch}>
				<AutoComplete
					autoFocus={true}
					autoComplete="off"
					panelClassName={styles.suggestions}
					style={{ flex: 1 }}
					inputClassName={styles.input}
					delay={0}
					variant="filled"
					placeholder="Search..."
					value={query}
					suggestions={autocomplete}
					completeMethod={() => { }}
					onSelect={handleComplete}
					onChange={handleChange}
				/>
				<button type="submit">Search</button>
			</form>
			{
				loading ? 
				(
					<div className={styles.loader_container}>
						<div className={styles.loader} />
					</div>
				) : searchResults && (
					<>
						{
							searchResults && searchResults?.did_you_mean ? (<p style={{cursor: "pointer", marginBottom: "0.5rem"}} onClick={handleDidYouMean}><i>Did you mean: <b>{searchResults.did_you_mean}</b></i></p>) : null
						}
						{
							searchResults && searchResults?.total_results ? (<p><i>Found <b>{searchResults.total_results}</b> total results </i></p>) : null
						}
						<Pagination onChange={handlePageChange} currentPage={currentPage} totalPages={searchResults?.total_pages} display={!!searchResults} />
						<div className={styles.results}>
							{
								searchResults && searchResults.results && (
									searchResults.results.length == 0 ? <p>No results found</p> : (
										searchResults.results.map((result, index) => (
											<div key={index} className={styles.result}>
												<p>{start + index}. on page: {result[0]}</p>
												<p>{result[1][0]}</p>
												<br />
												<hr />
												<br />
											</div>
										))
									)
								)
							}
						</div>
						<Pagination onChange={handlePageChange} currentPage={currentPage} totalPages={searchResults?.total_pages} display={!!searchResults} />
					</>)
			}
		</div>
	);
}

function Pagination({ currentPage, totalPages, display, onChange }) {
	const pages = useMemo(() => {
		if (!totalPages) {
			return [];
		}
		const pages = [];
		for (let i = Math.max(1, currentPage - 3); i <= Math.min(currentPage + 4, totalPages); i++) {
			pages.push(i);
		}
		return pages;
	}, [currentPage, totalPages]);

	if (!display) {
		return null;
	}

	return (
		<div className={styles.pagination}>
			{
				currentPage > 1 && (
					<>
						<span onClick={() => onChange(1)}><GrChapterPrevious size={13} /></span>
						<span onClick={() => onChange(Math.max(currentPage - 1, 1))}><GrCaretPrevious size={13} /></span>
					</>)
			}
			{
				pages[0] > 1 && (
					<span style={{ cursor: "default" }}>...</span>
				)
			}
			{
				pages.map((page, index) => (
					<span onClick={() => onChange(Math.min(Math.max(1, page), totalPages))} key={index} className={currentPage === page ? styles.active : ""}>{page}</span>
				))
			}
			{
				pages[pages.length - 1] < totalPages && (
					<span style={{ cursor: "default" }}>...</span>
				)
			}
			{
				currentPage < totalPages && (
					<>
						<span onClick={() => onChange(Math.min(currentPage + 1, totalPages))}><GrCaretNext size={13} /></span>
						<span onClick={() => onChange(totalPages)}><GrChapterNext size={13} /></span>
					</>
				)
			}
		</div>
	)
}

export default App;
