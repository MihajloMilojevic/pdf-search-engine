from .searches.word_search import WordSearch
from .searches.phrase_search import PhraseSearch
from .searches.and_expression import AndExpression
from .searches.or_expression import OrExpression
from .searches.not_expression import NotExpression
import re

class Parser:

    FRAZE_DELIMITER = '"'
    AND_OPERATOR = 'AND'
    OR_OPERATOR = 'OR'
    NOT_OPERATOR = 'NOT'
    GROUP_START = '('
    GROUP_END = ')'

    def __init__(self, query):
        self.query = query


    def parse(self):
        query = self.__clean_text(self.query)
        tokens = self.__tokenize(query)
        tokens = [self.__convert_to_word(token) for token in tokens]
        tokens = self.__combine_phrases(tokens)
        tokens = self.__add_ors(tokens)
        tokens = self.__extract_groups(tokens)
        return self.__parse_group(tokens)
        
    def __parse_group(self, group_tokens):
        stack = []
        postfix = []
        i = 0
        while i < len(group_tokens):
            if isinstance(group_tokens[i], list):
                postfix.append(self.__parse_group(group_tokens[i]))
            elif group_tokens[i] in [Parser.AND_OPERATOR, Parser.OR_OPERATOR, Parser.NOT_OPERATOR]:
                while len(stack) > 0 and self.__priority(stack[-1]) >= self.__priority(group_tokens[i]):
                    postfix.append(stack.pop())
                stack.append(group_tokens[i])
            else:
                postfix.append(group_tokens[i])
            i += 1
        while len(stack) > 0:
            postfix.append(stack.pop())
        return self.__build_expression(postfix)
    
    def __build_expression(self, postfix):
        stack = []
        try:
            for token in postfix:
                if token == Parser.AND_OPERATOR:
                    right = stack.pop()
                    left = stack.pop()
                    stack.append(AndExpression(left, right))
                elif token == Parser.OR_OPERATOR:
                    right = stack.pop()
                    left = stack.pop()
                    stack.append(OrExpression(left, right))
                elif token == Parser.NOT_OPERATOR:
                    right = stack.pop()
                    left = stack.pop()
                    stack.append(NotExpression(left, right))
                else:
                    stack.append(token)
        except IndexError:
            raise ValueError("The expression is not valid")
        if len(stack) != 1:
            raise ValueError("The expression is not valid")
        return stack[0]

    def __extract_groups(self, tokens):
        starts, ends = self.__find_groups(tokens)
        new_tokens = []
        i = 0
        while i < len(tokens):
            if i in starts:
                new_tokens.append(self.__combine_groups(tokens, i))
                i = ends[starts.index(i)]
            else:
                new_tokens.append(tokens[i])
            i += 1
        return new_tokens

    def __find_groups(self, tokens):
        groups_start = []
        groups_end = []
        i = 0
        count = 0
        start = 0
        while i < len(tokens):
            if tokens[i] == Parser.GROUP_START:
                if count == 0:
                    start = i
                count += 1
            if tokens[i] == Parser.GROUP_END:
                count -= 1
                if count == 0:
                    groups_start.append(start)
                    groups_end.append(i)
            if count < 0:
                raise ValueError("The group is not opened")
            i += 1
        if count > 0:
            raise ValueError("The group is not closed")
        return groups_start, groups_end

    def __combine_groups(self, tokens, start_index=0):
        if tokens[start_index] != Parser.GROUP_START:
            raise ValueError("The token at the start index must be a group start.")
        group = []
        i = start_index + 1
        while i < len(tokens):
            if tokens[i] == Parser.GROUP_START:
                group.append(self.__combine_groups(tokens, i))
            if tokens[i] == Parser.GROUP_END:
                return group
            
            group.append(tokens[i])
            i += 1
        if len(group) == 0:
            raise ValueError("The group is empty")
        raise ValueError("The group is not closed")
    
    def __add_ors(self, tokens):
        new_tokens = []
        for token in tokens:
            if len(new_tokens) == 0:
                new_tokens.append(token)
                continue
            # when not to insert OR
            # 1. when the last token is an operator
            # 2. when the current token is an operator
            # 3. when the last token is a group end
            # 4. when the current token is a group end
            if not (token in [Parser.AND_OPERATOR, Parser.OR_OPERATOR, Parser.NOT_OPERATOR, Parser.GROUP_END] or 
                    new_tokens[-1] in [Parser.AND_OPERATOR, Parser.OR_OPERATOR, Parser.NOT_OPERATOR, Parser.GROUP_START]):
                new_tokens.append(Parser.OR_OPERATOR)

            new_tokens.append(token)
        return new_tokens
    
    def __combine_phrases(self, tokens):
        new_tokens = []
        i = 0
        while i < len(tokens):
            if tokens[i] == Parser.FRAZE_DELIMITER:
                phrase = []
                i += 1
                while i < len(tokens) and tokens[i] != Parser.FRAZE_DELIMITER:
                    if tokens[i] in [Parser.GROUP_START, Parser.GROUP_END]:
                        raise ValueError("You can\' have groups inside a phrase. Found: " + tokens[i])
                    phrase.append(tokens[i])
                    i += 1
                if len(phrase) == 0:
                    continue
                new_tokens.append(PhraseSearch(phrase))
            else:
                new_tokens.append(tokens[i])
            i += 1
        return new_tokens

    def __clean_text(self, text):
        # Define the regex pattern to match all characters except letters, parentheses, and double quotes
        pattern = r'[^a-zA-Z()"]'
        text = re.sub(pattern, ' ', text)
        text = re.sub(r'\s+', ' ', text)    
        return text.strip()

    def __tokenize(self, text):
        pattern = r'\s+|(?=[()"])|(?<=[()"])'
        parts = re.split(pattern, text)
        parts = [part for part in parts if part.strip()]
        return parts
    
    def __convert_to_word(self, token):
        if token in [Parser.AND_OPERATOR, Parser.OR_OPERATOR, Parser.NOT_OPERATOR, Parser.GROUP_START, Parser.GROUP_END, Parser.FRAZE_DELIMITER]:
            return token
        return WordSearch(token)
    
    def __priority(self, operator):
        if operator == Parser.NOT_OPERATOR:
            return 3
        if operator == Parser.AND_OPERATOR:
            return 2
        if operator == Parser.OR_OPERATOR:
            return 1
        return 0
    
