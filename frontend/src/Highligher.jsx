import React from "react";

function isSearchedWord(word, allWords) {
    return allWords.some(w => w.toLowerCase() === word.toLowerCase());
}

function splitTextByWords(text, words) {
    // Create a regex pattern that matches any of the words
    const pattern = new RegExp(`(${words.map(word => word.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&')).join('|')})`, 'gi');
    
    // Split the text by the pattern
    const splitText = text.split(pattern);
    
    // Filter out any empty strings resulting from the split
    const filtered = splitText.filter(part => part.trim().length > 0);
    
    const result = [];
    let i = 0;
    while ( i < filtered.length) {
        let part = filtered[i];
        if (isSearchedWord(part, words)) {
            let text = part;
            i++;
            while (i < filtered.length && isSearchedWord(filtered[i], words)) {
                text += " " + filtered[i];
                i++;
            }
            result.push([text, true]);
        } else {
            result.push([part, false]);
            i++;
        }
    }
    
    return result;
}

export default function Highlighter({text, words}) {
    return (
        <>
        {
            splitTextByWords(text, words).map(([part, isHighlighted], index) => {
                if (isHighlighted) {
                    return <mark key={index}>{part}</mark>;
                } else {
                    return <span key={index}>{part}</span>;
                }
            })
        }
        </>
    );
} 