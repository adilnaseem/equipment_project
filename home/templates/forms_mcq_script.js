function createGoogleForm() {
    // Create a new form
    const form = FormApp.create('Radio Communication MCQs');
    
    // Add questions to the form
    const questions = [
      {
        title: 'What is the correct configuration of walkie talkie in PTB?',
        choices: ['Zone 1, Channel 2', 'Zone 2, Channel 3', 'Analogue, Channel Digital', 'Analogue, Channel 4'],
        correctAnswer: 'Analogue, Channel 4'
      },


      





      {
        title: 'In PTB we have (select more than one)',
        choices: ['Zone 1', 'Zone 2', 'Analogue', 'Digital'],
        correctAnswers: ['Zone 1', 'Analogue'],
        type: 'checkbox'
      },
      {
        title: 'Which model of Hytera is mostly being used at AIIAP',
        choices: ['P688G', 'P788G', 'P888G', 'P988H'],
        correctAnswer: 'P788G'
      },
      {
        title: 'At perimeter the channel is',
        choices: ['2', '3', '4', '1'],
        correctAnswer: '3'
      },
      {
        title: 'In PTB parking we have',
        choices: ['Zone 4', 'Zone 3', 'Digital 3', 'Zone 1'],
        correctAnswer: 'Zone 1'
      },
      {
        title: 'What is the primary function of a repeater in a communication system?',
        choices: ['Amplify the audio signal', 'Extend the range of communication', 'Encrypt the communication', 'Reduce interference'],
        correctAnswer: 'Extend the range of communication'
      },
      {
        title: 'What does DMR stand for in communication systems?',
        choices: ['Digital Mobile Radio', 'Dynamic Mobile Range', 'Data Multiplexing Radio', 'Dual Mode Radio'],
        correctAnswer: 'Digital Mobile Radio'
      },
      {
        title: 'What component is responsible for converting voice into electrical signals in a walkie-talkie?',
        choices: ['Antenna', 'Microphone', 'Speaker', 'Transmitter'],
        correctAnswer: 'Microphone'
      },
      {
        title: 'Which battery type is commonly used in Hytera walkie-talkies?',
        choices: ['Ni-Cd', 'Ni-MH', 'Lithium-ion', 'Alkaline'],
        correctAnswer: 'Lithium-ion'
      },
      {
        title: 'What does the PTT button stand for in a walkie-talkie?',
        choices: ['Push To Talk', 'Press To Transmit', 'Power Transmit Tool', 'Pause To Talk'],
        correctAnswer: 'Push To Talk'
      },
      {
        title: 'What could cause a walkie-talkie not to transmit or receive signals?',
        choices: ['Faulty antenna', 'Incorrect frequency setting', 'Dead battery', 'All of the above'],
        correctAnswer: 'All of the above'
      },
      {
        title: 'What is the maximum communication range of the Hytera P788G in an open area?',
        choices: ['1-2 km', '5-8 km', '10-12 km', '15-20 km'],
        correctAnswer: '10-12 km'
      },
      {
        title: 'Which Hytera feature allows users to track the location of a radio?',
        choices: ['GPS', 'Bluetooth', 'Wi-Fi', 'NFC'],
        correctAnswer: 'GPS'
      },
      {
        title: 'What is the typical charging time for a Hytera Lithium-Ion battery?',
        choices: ['1-2 hours', '3-4 hours', '5-6 hours', '7-8 hours'],
        correctAnswer: '3-4 hours'
      },
      {
        title: 'What is the typical lifespan of a Hytera Lithium-Ion battery under normal usage?',
        choices: ['6 months', '1 year', '2-3 years', '5 years'],
        correctAnswer: '2-3 years'
      },
      {
        title: 'Which of the following is an example of preventive maintenance for Hytera radios?',
        choices: ['Replacing a faulty speaker', 'Regularly cleaning the connectors', 'Resetting the device to factory settings', 'Performing firmware updates after issues arise'],
        correctAnswer: 'Regularly cleaning the connectors'
      },
      {
        title: 'Which component is typically checked first during functional testing of a walkie-talkie?',
        choices: ['Antenna', 'Battery', 'Speaker', 'Display'],
        correctAnswer: 'Battery'
      },
      {
        title: 'Which of the following is a recommended practice for cleaning the Hytera P788G?',
        choices: ['Use water and soap', 'Use a dry or slightly damp lint-free cloth', 'Use alcohol-based cleaning solutions directly on the device', 'Avoid cleaning the device to prevent damage'],
        correctAnswer: 'Use a dry or slightly damp lint-free cloth'
      },
      {
        title: 'Communication network is necessary for Walkie Talkie communication', // True/False question
        choices: ['True', 'False'],
        correctAnswer: 'True'
      }
    ];
    
    questions.forEach(function(question) {
      if (question.type === 'checkbox') {
        const checkboxItem = form.addCheckboxItem();
        checkboxItem.setTitle(question.title)
            .setChoices(question.choices.map(choice => checkboxItem.createChoice(choice, question.correctAnswers.includes(choice))));
      } else {
        const multipleChoiceItem = form.addMultipleChoiceItem();
        multipleChoiceItem.setTitle(question.title)
            .setChoices(question.choices.map(choice => multipleChoiceItem.createChoice(choice, choice === question.correctAnswer)));
      }
    });
    
    Logger.log('Form created with ID: ' + form.getId());
  }