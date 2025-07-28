// App.js
import React, { useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { ThemeProvider } from './theme';
import HomeScreen from './screens/Home';
import ProjectScreen from './screens/Project';
import SettingsScreen from './screens/Settings';

const Stack = createStackNavigator();

export default function App() {
  return (
    <ThemeProvider>
      <NavigationContainer>
        <Stack.Navigator>
          <Stack.Screen name="Home" component={HomeScreen} />
          <Stack.Screen name="Project" component={ProjectScreen} />
          <Stack.Screen name="Settings" component={SettingsScreen} />
        </Stack.Navigator>
      </NavigationContainer>
    </ThemeProvider>
  );
}

// screens/Home.js
export default function HomeScreen() {
  const [prompt, setPrompt] = useState('');
  
  const handleGenerate = async () => {
    try {
      const response = await fetch('api/generate', {
        method: 'POST',
        body: JSON.stringify({ prompt })
      });
      // Handle response
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <View style={styles.container}>
      <TextInput
        value={prompt}
        onChangeText={setPrompt}
        placeholder="Enter your project idea..."
        multiline
      />
      <Button title="Generate" onPress={handleGenerate} />
    </View>
  );
}
