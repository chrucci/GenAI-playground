import unittest
from memory import conversational_buffer as cb
from langchain.schema.messages import HumanMessage, AIMessage 


class TestConversationalBuffer(unittest.TestCase):
    
    
    
    def get_input(self, input_string):
        return {"input": input_string}
    
    def get_output(self, output_string):
        return {"output": output_string}
    
    # test load_mem, assert that the memory that's passed in is also returned.
    def test_load_mem_returns_mem_var(self):
        input_string = "hi"
        output_string = "whats up"
        input = self.get_input(input_string)
        output = self.get_output(output_string)
        actual = cb.load_mem(input, output)
        exp_message = f"Human: {input_string}\nAI: {output_string}"
        expected = {'history': exp_message}
        self.assertEqual(expected, actual)

    def test_load_mem_return__with_message__returns_message_history(self):
        input_string = "hi"
        output_string = "whats up"
        input = self.get_input(input_string)
        output = self.get_output(output_string)
        expected =   {'history': [HumanMessage(content=input_string), AIMessage(content=output_string)]}
        actual = cb.load_mem_return(input, output)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
