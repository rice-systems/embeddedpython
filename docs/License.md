Owl is the product of several years of development by the Rice Computer Architecture Group at Rice University and a collection of wonderful open-source software projects. Combined, they provide an open-source environment for programming microcontrollers that is free and easy to use.

This release combines work from:

-   [Dean Hall's Python-on-a-Chip](http://code.google.com/p/python-on-a-chip/)
-   [libffi](http://sourceware.org/libffi/)
-   [Python 2.7](http://python.org/)
-   [libopencm3](http://www.libopencm3.org/)
-   [Texas Instruments Stellaris Driverlib](http://www.ti.com/tool/sw-lm3s)

Each source file contains a header that explains the license that applies to that particular file. The majority of the system, including the complete virtual machine and Python library, is provided under the MIT license. The FFI subsystem is provided under the libffi license, which is identical to the MIT license.

However, some support code, including but not limited to the linker scripts for the Stellaris microcontrollers, is provided under the GNU Lesser GPL. This license is compatible with the MIT license with some exceptions.

Owl links in portions of Driverlib and USBlib, the peripheral driver libraries distributed as a part of Texas Instrument's Stellarisware. Driverlib is provided by TI under the BSD license, and USBlib is provided under a proprietary, re-distributable license.

Any user wishing to redistribute Owl should ensure that he or she is complying with the licenses for all the code contained therein. For reference, the various licenses used in this project are quoted here. This document should not be considered to be authoritative; the license statements in each file should be used for reference:

MIT License (Core VM, toolchain, libraries)
-------------------------------------------

Copyright 2003, 2006, 2007, 2009 Dean Hall.

Copyright 2010-2013 Rice University.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

libffi license (FFI subsystem)
------------------------------

libffi - Copyright (c) 1996-2012 Anthony Green, Red Hat, Inc and others. See source files for details.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \`\`Software*), to deal in the Software without restriction, including* without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED \`\`AS IS*, WITHOUT WARRANTY OF ANY KIND,* EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

GNU Lesser General Public License (Version 3, Linker script, initialization routines)
-------------------------------------------------------------------------------------

GNU LESSER GENERAL PUBLIC LICENSE Version 3, 29 June 2007

Copyright (C) 2007 Free Software Foundation, Inc. &lt;[1](http://fsf.org/)&gt; Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.

This version of the GNU Lesser General Public License incorporates the terms and conditions of version 3 of the GNU General Public License, supplemented by the additional permissions listed below.

0. Additional Definitions.

As used herein, “this License” refers to version 3 of the GNU Lesser General Public License, and the “GNU GPL” refers to version 3 of the GNU General Public License.

“The Library” refers to a covered work governed by this License, other than an Application or a Combined Work as defined below.

An “Application” is any work that makes use of an interface provided by the Library, but which is not otherwise based on the Library. Defining a subclass of a class defined by the Library is deemed a mode of using an interface provided by the Library.

A “Combined Work” is a work produced by combining or linking an Application with the Library. The particular version of the Library with which the Combined Work was made is also called the “Linked Version”.

The “Minimal Corresponding Source” for a Combined Work means the Corresponding Source for the Combined Work, excluding any source code for portions of the Combined Work that, considered in isolation, are based on the Application, and not on the Linked Version.

The “Corresponding Application Code” for a Combined Work means the object code and/or source code for the Application, including any data and utility programs needed for reproducing the Combined Work from the Application, but excluding the System Libraries of the Combined Work.

1. Exception to Section 3 of the GNU GPL.

You may convey a covered work under sections 3 and 4 of this License without being bound by section 3 of the GNU GPL.

2. Conveying Modified Versions.

If you modify a copy of the Library, and, in your modifications, a facility refers to a function or data to be supplied by an Application that uses the facility (other than as an argument passed when the facility is invoked), then you may convey a copy of the modified version:

a) under this License, provided that you make a good faith effort to ensure that, in the event an Application does not supply the unction or data, the facility still operates, and performs whatever part of its purpose remains meaningful, or

b) under the GNU GPL, with none of the additional permissions of this License applicable to that copy.

3. Object Code Incorporating Material from Library Header Files.

The object code form of an Application may incorporate material from a header file that is part of the Library. You may convey such object code under terms of your choice, provided that, if the incorporated material is not limited to numerical parameters, data structure layouts and accessors, or small macros, inline functions and templates (ten or fewer lines in length), you do both of the following:

a) Give prominent notice with each copy of the object code that the Library is used in it and that the Library and its use are covered by this License.

b) Accompany the object code with a copy of the GNU GPL and this license document.

4. Combined Works.

You may convey a Combined Work under terms of your choice that, taken together, effectively do not restrict modification of the portions of the Library contained in the Combined Work and reverse engineering for debugging such modifications, if you also do each of the following:

a) Give prominent notice with each copy of the Combined Work that the Library is used in it and that the Library and its use are covered by this License.

b) Accompany the Combined Work with a copy of the GNU GPL and this license document.

c) For a Combined Work that displays copyright notices during execution, include the copyright notice for the Library among these notices, as well as a reference directing the user to the copies of the GNU GPL and this license document.

d) Do one of the following:

0) Convey the Minimal Corresponding Source under the terms of this License, and the Corresponding Application Code in a form suitable for, and under terms that permit, the user to recombine or relink the Application with a modified version of the Linked Version to produce a modified Combined Work, in the manner specified by section 6 of the GNU GPL for conveying Corresponding Source.

1) Use a suitable shared library mechanism for linking with the Library. A suitable mechanism is one that (a) uses at run time a copy of the Library already present on the user's computer system, and (b) will operate properly with a modified version of the Library that is interface-compatible with the Linked Version.

e) Provide Installation Information, but only if you would otherwise be required to provide such information under section 6 of the GNU GPL, and only to the extent that such information is necessary to install and execute a modified version of the Combined Work produced by recombining or relinking the Application with a modified version of the Linked Version. (If you use option 4d0, the Installation Information must accompany the Minimal Corresponding Source and Corresponding Application Code. If you use option 4d1, you must provide the Installation Information in the manner specified by section 6 of the GNU GPL for conveying Corresponding Source.)

5. Combined Libraries.

You may place library facilities that are a work based on the Library side by side in a single library together with other library facilities that are not Applications and are not covered by this License, and convey such a combined library under terms of your choice, if you do both of the following:

a) Accompany the combined library with a copy of the same work based on the Library, uncombined with any other library facilities, conveyed under the terms of this License.

b) Give prominent notice with the combined library that part of it is a work based on the Library, and explaining where to find the accompanying uncombined form of the same work.

6. Revised Versions of the GNU Lesser General Public License.

The Free Software Foundation may publish revised and/or new versions of the GNU Lesser General Public License from time to time. Such new versions will be similar in spirit to the present version, but may differ in detail to address new problems or concerns.

Each version is given a distinguishing version number. If the Library as you received it specifies that a certain numbered version of the GNU Lesser General Public License “or any later version” applies to it, you have the option of following the terms and conditions either of that published version or of any later version published by the Free Software Foundation. If the Library as you received it does not specify a version number of the GNU Lesser General Public License, you may choose any version of the GNU Lesser General Public License ever published by the Free Software Foundation.

If the Library as you received it specifies that a proxy can decide whether future versions of the GNU Lesser General Public License shall apply, that proxy's public statement of acceptance of any version is permanent authorization for you to choose that version for the Library.

BSD License (driverlib)
-----------------------

Software License Agreement

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the original copyright notice, this list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the original copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

Neither the name of Texas Instruments Incorporated nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

TI USBlib license
-----------------

TI StellarisWare Clickwrap Software License Agreement (SLA)

Important - This is a legally binding agreement. Read it carefully. After you read the following terms, you will be asked whether you are authorized to commit your company to abide by the following terms. THIS AGREEMENT IS DISPLAYED FOR YOU TO READ PRIOR TO DOWNLOADING OR USING THE “LICENSED MATERIALS”.

DO NOT DOWNLOAD OR INSTALL the software programs unless you agree on behalf of yourself and your company to be bound by the terms of this License Agreement.

DO NOT CLICK “I AGREE” UNLESS:

1. YOU ARE AUTHORIZED TO AGREE TO THE TERMS OF THIS LICENSE ON BEHALF OF YOURSELF AND YOUR COMPANY; AND

2. YOU INTEND TO ENTER THIS LEGALLY BINDING AGREEMENT ON BEHALF OF YOURSELF AND YOUR COMPANY.

Important - Read carefully: This software license agreement (“Agreement”) is a legal agreement between you (either an individual or entity) and Texas Instruments Incorporated (“TI”). The “Licensed Materials” subject to this Agreement include the software programs TI has granted you access to download and any “on-line” or electronic documentation associated with these programs, or any portion thereof, and may also include hardware, reference designs and associated documentation. The Licensed Materials are specifically designed and licensed for use solely and exclusively with microprocessor/microcontroller devices manufactured by or for TI (“TI Devices”). By installing, copying or otherwise using the Licensed Materials you agree to abide by the provisions set forth herein. This Agreement is displayed for you to read prior to using the Licensed Materials. If you choose not to accept or agree with these provisions, do not download or install the Licensed Materials.

1. Delivery. TI may deliver the Licensed Materials, or portions thereof, to you electronically.

2. License Grant and Use Restrictions.

a. Limited Source Code License. Subject to the terms of this Agreement, and commencing as of the Effective Date and continuing for the term of this Agreement, TI hereby grants to you a limited, free, non-transferable, non-exclusive, non-assignable, non-sub-licensable license to make copies, prepare derivative works, display internally and use internally the Licensed Materials provided to you in source code for the sole purposes of designing and developing object and executable versions of such Licensed Materials or any derivative thereof, that execute solely and exclusively on TI Devices used in Customer Product(s), and maintaining and supporting such Licensed Materials, or any derivative thereof, and Customer Product(s). “Customer Product” means a final product distributed by or for you that consists of both hardware, including one or more TI Devices, and software components, including only executable versions of the Licensed Materials that execute solely and exclusively on or with such TI Devices and not on devices manufactured by or for an entity other than TI.

b. Production and Distribution License. Subject to the terms of this Agreement, and commencing as of the Effective Date and continuing for the term of this Agreement, TI hereby grants to you a free, non-exclusive, non-transferable, non-assignable, worldwide license to:

(i). Use object code versions of the Licensed Materials, or any derivative thereof, to make copies, display internally, evaluate, test, distribute internally and use internally for the sole purposes of designing and developing Customer Product(s), and maintaining and supporting the Licensed Materials and Customer Product(s);

(ii). Make copies, use, sell, offer to sell, and otherwise distribute object code and executable versions of the Licensed Materials, or any derivative thereof, for use in or with Customer Product(s), provided that such Licensed Materials are embedded in or only used with Customer Product(s), and provided further that such Licensed Materials execute solely and exclusively on a TI Device and not on any device manufactured by or for an entity other than TI.

c. Demonstration License. Subject to the terms of this Agreement, and commencing as of the Effective Date and continuing for the term of this Agreement, TI grants to you a free, non-transferable, non-exclusive, non-assignable, non-sub-licensable worldwide license to demonstrate to third parties the Licensed Materials as they are used in Customer Products executing solely and exclusively on TI Devices, provided that such Licensed Materials are demonstrated in object or executable versions only.

d. Reference Design Use License. Subject to the terms of this Agreement, and commencing as of the Effective Date and continuing for the term of this Agreement, TI hereby grants to you a free, non-transferable, non-exclusive, non-assignable, non-sub-licensable worldwide license to:

(i). use the Licensed Materials to design, develop, manufacture or have manufactured, sell, offer to sell, or otherwise distribute Customer Product(s) or product designs, including portions or derivatives of the Licensed Materials as they are incorporated in or used with Customer Product(s), provided such Customer Products or product designs utilize a TI Device.

e. Contractors and Suppliers. The licenses granted to you hereunder shall include your on-site and off-site suppliers and independent contractors, while such suppliers and independent contractors are performing work for or providing services to you, provided that such suppliers and independent contractors have executed work-for-hire agreements with you containing terms and conditions not inconsistent with the terms and conditions set forth is this Agreement and provided further that such contractors may provide work product to only you under such work-for-hire agreements.

f. No Other License. Notwithstanding anything to the contrary, nothing in this Agreement shall be construed as a license to any intellectual property rights of TI other than those rights embodied in the Licensed Materials provided to you by TI. EXCEPT AS PROVIDED HEREIN, NO OTHER LICENSE, EXPRESS OR IMPLIED, BY ESTOPPEL OR OTHERWISE, TO ANY OTHER TI INTELLECTUAL PROPERTY RIGHTS IS GRANTED HEREIN.

g. Restrictions. You shall maintain the source code versions of the Licensed Materials under password control protection and shall not disclose such source code versions of the Licensed Materials, or any derivative thereof, to any person other than your employees and contractors whose job performance requires access. You shall not use the Licensed Materials with a processing device manufactured by or for an entity other than TI, and you agree that any such unauthorized use of the Licensed Materials is a material breach of this Agreement. Except as expressly provided in this Agreement, you shall not copy, publish, disclose, display, provide, transfer or make available the Licensed Materials to any third party and you shall not sublicense, transfer, or assign the Licensed Materials or your rights under this Agreement to any third party. You shall not mortgage, pledge or encumber the Licensed Materials in any way. You shall not (i) incorporate, combine, or distribute the Licensed Materials, or any derivative thereof, with any Public Software, or (ii) use Public Software in the development of any derivatives of the Licensed Materials, each in such a way that would cause the Licensed Materials, or any derivative thereof, to be subject to all or part of the license obligations or other intellectual property related terms with respect to such Public Software, including but not limited to, the obligations that the Licensed Materials, or any derivative thereof, incorporated into, combined, or distributed with such Public Software (x) be disclosed or distributed in source code form, be licensed for the purpose of making derivatives of such software, or be redistributed free of charge, contrary to the terms and conditions of this Agreement, (y) be used with devices other than TI Devices, or (z) be otherwise used or distributed in a manner contrary to the terms and conditions of this Agreement. As used in this Section 2(g), “Public Software” means any software that contains, or is derived in whole or in part from, any software distributed as open source software, including but not limited to software licensed under the following or similar models: (A) GNU's General Public License (GPL) or Lesser/Library GPL (LGPL), (B) the Artistic License (e.g., PERL), (C) the Mozilla Public License, (D) the Netscape Public License, (E) the Sun Community Source License (SCSL), (F) the Sun Industry Standards Source License (SISL), (G) the Apache Server license, (H) QT Free Edition License, (I) IBM Public License, and (J) BitKeeper.

h. Termination. This Agreement is effective until terminated. You may terminate this Agreement at any time by written notice to TI. Without prejudice to any other rights, if you fail to comply with the terms of this Agreement, TI may terminate your right to use the Licensed Materials upon written notice to you. Upon termination of this Agreement, you will destroy any and all copies of the Licensed Materials in your possession, custody or control and provide to TI a written statement signed by your authorized representative certifying such destruction. The following sections will survive any expiration or termination of this Agreement: 2(h) (Termination), 3 (Licensed Materials Ownership), 6 (Warranties and Limitations), 7 (Indemnification Disclaimer), 10 (Export Control), 11 (Governing Law and Severability), 12 (PRC Provisions), and 13 (Entire Agreement). The obligations set forth in Section 5 (Confidential Information) will survive any expiration or termination of this Agreement for three (3) years after such expiration or termination.

3. Licensed Materials Ownership. The Licensed Materials are licensed, not sold to you, and can only be used in accordance with the terms of this Agreement. Subject to the licenses granted to you pursuant to this Agreement, TI and TI's licensors own and shall continue to own all right, title, and interest in and to the Licensed Materials, including all copies thereof. The parties agree that all fixes, modifications and improvements to the Licensed Materials conceived of or made by TI that are based, either in whole or in part, on your feedback, suggestions or recommendations are the exclusive property of TI and all right, title and interest in and to such fixes, modifications or improvements to the Licensed Materials will vest solely in TI. Moreover, you acknowledge and agree that when your independently developed software or hardware components are combined, in whole or in part, with the Licensed Materials, your right to use the Licensed Materials embodied in such resulting combined work shall remain subject to the terms and conditions of this Agreement.

4. Intellectual Property Rights.

a. The Licensed Materials contain copyrighted material, trade secrets and other proprietary information of TI and TI's licensors and are protected by copyright laws, international copyright treaties, and trade secret laws, as well as other intellectual property laws. To protect TI's and TI's licensors' rights in the Licensed Materials, you agree, except as specifically permitted by statute by a provision that cannot be waived by contract, not to “unlock”, decompile, reverse engineer, disassemble or otherwise translate any portions of the Licensed Materials to a human-perceivable form nor to permit any person or entity to do so. You shall not remove, alter, cover, or obscure any confidentiality, trade secret, proprietary, or copyright notices, trade-marks, proprietary, patent, or other identifying marks or designs from any component of the Licensed Materials and you shall reproduce and include in all copies of the Licensed Materials the copyright notice(s) and proprietary legend(s) of TI and TI's licensors as they appear in the Licensed Materials. TI reserves all rights not specifically granted under this Agreement.

b. Third parties may claim to own patents, copyrights, or other intellectual property rights that cover the implementation of certain Licensed Materials. Certain Licensed Materials may also be based on industry recognized standards, including but not limited to specifically the ISO MPEG and ITU standards, and software programs published by industry recognized standards bodies and certain third parties claim to own patents, copyrights, and other intellectual property rights that cover implementation of those standards. You acknowledge and agree that this Agreement does not convey a license to any such third party patents, copyrights, and other intellectual property rights and that you are solely responsible for any patent, copyright, or other intellectual property right claims that relate to your use and distribution of the Licensed Materials, and your use and distribution of your products that include or incorporate the Licensed Materials.

5. Confidential Information. You acknowledge and agree that the Licensed Materials contain trade secrets and other confidential information of TI and TI's licensors. You agree to use the Licensed Materials solely within the scope of the licenses set forth herein, to maintain the Licensed Materials in strict confidence, to use at least the same procedures and degree of care that you use to prevent disclosure of your own confidential information of like importance but in no instance less than reasonable care, and to prevent disclosure of the Licensed Materials to any third party, except as may be necessary and required in connection with your rights and obligations hereunder. You agree to obtain executed confidentiality agreements with your employees and contractors having access to the Licensed Materials and to diligently take steps to enforce such agreements in this respect. TI agrees that the employment agreements used in the normal course of your business shall satisfy the requirements of this section. TI may disclose your contact information to TI's applicable licensors.

6. Warranties and Limitations. YOU ACKNOWLEDGE AND AGREE THAT THE LICENSED MATERIALS MAY NOT BE INTENDED FOR PRODUCTION APPLICATIONS AND MAY CONTAIN IRREGULARITIES AND DEFECTS NOT FOUND IN PRODUCTION SOFTWARE. FURTHERMORE, YOU ACKNOWLEDGE AND AGREE THAT THE LICENSED MATERIALS HAVE NOT BEEN TESTED OR CERTIFIED BY ANY GOVERNMENT AGENCY OR INDUSTRY REGULATORY ORGANIZATION OR ANY OTHER THIRD PARTY ORGANIZATION. YOU AGREE THAT PRIOR TO USING, INCORPORATING OR DISTRIBUTING THE LICENSED MATERIALS IN OR WITH ANY COMMERCIAL PRODUCT THAT YOU WILL THOROUGHLY TEST THE PRODUCT AND THE FUNCTIONALITY OF THE LICENSED MATERIALS IN OR WITH THAT PRODUCT AND BE SOLELY RESPONSIBLE FOR ANY PROBLEMS OR FAILURES.

THE LICENSED MATERIALS AND ANY REALTED DOCUMENTATION ARE PROVIDED “AS IS” AND WITH ALL FAULTS. TI MAKES NO WARRANTY OR REPRESENTATION, WHETHER EXPRESS, IMPLIED OR STATUTORY, REGARDING THE LICENSED MATERIALS, INCLUDING BUT NOT LIMITED TO, ANY IMPLIED WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE, LACK OF VIRUSES, ACCURACY OR COMPLETENESS OF RESPONSES, RESULTS AND LACK OF NEGLIGENCE. TI DISCLAIMS ANY WARRANTY OF TITLE, QUIET ENJOYMENT, QUIET POSSESSION, AND NON-INFRINGEMENT OF ANY THIRD PARTY PATENTS, COPYRIGHTS, TRADE SECRETS OR OTHER INTELLECTUAL PROPERTY RIGHTS. YOU AGREE TO USE YOUR INDEPENDENT JUDGMENT IN DEVELOPING YOUR PRODUCTS. NOTHING CONTAINED IN THIS AGREEMENT WILL BE CONSTRUED AS A WARRANTY OR REPRESENTATION BY TI TO MAINTAIN PRODUCTION OF ANY TI SEMICONDUCTOR DEVICE OR OTHER HARDWARE OR SOFTWARE WITH WHICH THE LICENSED MATERIALS MAY BE USED.

IN NO EVENT SHALL TI, OR ANY APPLICABLE LICENSOR, BE LIABLE FOR ANY SPECIAL, INDIRECT, INCIDENTAL, PUNITIVE OR CONSEQUENTIAL DAMAGES, HOWEVER CAUSED, ON ANY THEORY OF LIABILITY, IN CONNECTION WITH OR ARISING OUT OF THIS AGREEMENT OR THE USE OF THE LICENSED MATERIALS, REGARDLESS OF WHETHER TI HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. EXCLUDED DAMAGES INCLUDE, BUT ARE NOT LIMITED TO, COST OF REMOVAL OR REINSTALLATION, OUTSIDE COMPUTER TIME, LABOR COSTS, LOSS OF DATA, LOSS OF GOODWILL, LOSS OF PROFITS, LOSS OF SAVINGS, OR LOSS OF USE OR INTERRUPTION OF BUSINESS. IN NO EVENT WILL TI'S AGGREGATE LIABILITY UNDER THIS AGREEMENT OR ARISING OUT OF YOUR USE OF THE LICENSED MATERIALS EXCEED FIVE HUNDRED U.S. DOLLARS (US$500). THE EXISTENCE OF MORE THAN ONE CLAIM WILL NOT ENLARGE OR EXTEND THESE LIMITS.

Because some jurisdictions do not allow the exclusion or limitation of incidental or consequential damages or limitation on how long an implied warranty lasts, the above limitations or exclusions may not apply to you.

7. Indemnification Disclaimer. YOU ACKNOWLEDGE AND AGREE THAT TI SHALL NOT BE LIABLE FOR AND SHALL NOT DEFEND OR INDEMNIFY YOU AGAINST ANY THIRD PARTY INFRINGEMENT CLAIM THAT RELATES TO OR IS BASED ON YOUR MANUFACTURE, USE, OR DISTRIBUTION OF THE LICENSED MATERIALS OR YOUR MANUFACTURE, USE, OFFER FOR SALE, SALE, IMPORTATION OR DISTRIBUTION OF YOUR PRODUCTS THAT INCLUDE OR INCORPORATE THE LICENSED MATERIALS.

You will defend and indemnify TI in the event of claim, liability or costs (including reasonable attorney's fees related to Your use or any sub-licensee's use of the Licensed Materials) relating in any way to Your violation of the terms of the License Grants set forth in Section 2, or any other violation of other terms and conditions of this Agreement.

8. No Technical Support. TI and TI's licensors are under no obligation to install, maintain or support the Licensed Materials.

9. Notices. All notices to TI hereunder shall be delivered to Texas Instruments Incorporated, AEC Software Operations, 12203 Southwest Freeway, Mail Station 701, Stafford, Texas 77477, Attention: Administrator, AEC Software Operations, with a copy to Texas Instruments Incorporated, 12203 Southwest Freeway, Mail Station 725, Stafford, Texas 77477, Attention: Legal Department. All notices shall be deemed served when received by TI.

10. Export Control. You hereby acknowledge that the Licensed Materials are subject to export control under the U.S. Commerce Department's Export Administration Regulations (“EAR”). You further hereby acknowledge and agree that unless prior authorization is obtained from the U.S. Commerce Department, neither you nor your customers will export, re-export, or release, directly or indirectly, any technology, software, or software source code (as defined in Part 772 of the EAR), received from TI, or export, directly or indirectly, any direct product of such technology, software, or software source code (as defined in Part 734 of the EAR), to any destination or country to which the export, re-export, or release of the technology, software, or software source code, or direct product is prohibited by the EAR. You agree that none of the Licensed Materials may be downloaded or otherwise exported or reexported (i) into (or to a national or resident of) Cuba, Iran, North Korea, Sudan and Syria or any other country the U.S. has embargoed goods; or (ii) to anyone on the U.S. Treasury Department's List of Specially Designated Nationals or the U.S. Commerce Department's Denied Persons List or Entity List. You represent and warrant that you are not located in, under the control of, or a national or resident of any such country or on any such list and you will not use or transfer the Licensed Materials for use in any sensitive nuclear, chemical or biological weapons, or missile technology end-uses unless authorized by the U.S. Government by regulation or specific license or for a military end-use in, or by any military entity of Albania, Armenia, Azerbaijan, Belarus, Cambodia, China, Georgia, Iran, Iraq, Kazakhstan, Kyrgyzstan, Laos, Libya, Macau, Moldova, Mongolia, Russia, Tajikistan, Turkmenistan, Ukraine, Uzbekistan, and Vietnam. Any software export classification made by TI shall be for TI's internal use only and shall not be construed as a representation or warranty regarding the proper export classification for such software or whether an export license or other documentation is required for the exportation of such software.

11. Governing Law and Severability. This Agreement will be governed by and interpreted in accordance with the laws of the State of Texas, without reference to conflict of laws principles. If for any reason a court of competent jurisdiction finds any provision of the Agreement to be unenforceable, that provision will be enforced to the maximum extent possible to effectuate the intent of the parties, and the remainder of the Agreement shall continue in full force and effect. This Agreement shall not be governed by the United Nations Convention on Contracts for the International Sale of Goods, or by the Uniform Computer Information Transactions Act (UCITA), as it may be enacted in the State of Texas. The parties agree that non-exclusive jurisdiction for any dispute arising out of or relating to this Agreement lies within the courts located in the State of Texas. Notwithstanding the foregoing, any judgment may be enforced in any United States or foreign court, and either party may seek injunctive relief in any United States or foreign court.

12. PRC Provisions. If you are located in the People's Republic of China (“PRC”) or if the Licensed Materials will be sent to the PRC, the following provisions shall apply and shall supersede any other provisions in this Agreement concerning the same subject matter as the following provisions:

a. Registration Requirements. You shall be solely responsible for performing all acts and obtaining all approvals that may be required in connection with this Agreement by the government of the PRC, including but not limited to registering pursuant to, and otherwise complying with, the PRC Measures on the Administration of Software Products, Management Regulations on Technology Import-Export, and Technology Import and Export Contract Registration Management Rules. Upon receipt of such approvals from the government authorities, you shall forward evidence of all such approvals to TI for its records. In the event that you fail to obtain any such approval or registration, you shall be solely responsible for any and all losses, damages or costs resulting therefrom, and shall indemnify TI for all such losses, damages or costs.

b. Governing Language. This Agreement is written and executed in the English language. If a translation of this Agreement is required for any purpose, including but not limited to registration of the Agreement pursuant to any governmental laws, regulations or rules, you shall be solely responsible for creating such translation. Any translation of this Agreement into a language other than English is intended solely in order to comply with such laws or for reference purposes, and the English language version shall be authoritative and controlling.

c. Export Control.

(i). Diversions of Technology. You hereby agree that unless prior authorization is obtained from the U.S. Department of Commerce, neither you nor your subsidiaries or affiliates shall knowingly export, re-export, or release, directly or indirectly, any technology, software, or software source code (as defined in Part 772 of the Export Administration Regulations of the U.S. Department of Commerce (“EAR”)), received from TI or any of its affiliated companies, or export, directly or indirectly, any direct product of such technology, software, or software source code (as defined in Part 734 of the EAR), to any destination or country to which the export, re-export, or release of the technology, software, software source code, or direct product is prohibited by the EAR.

(ii). Assurance of Compliance. You understand and acknowledge that products, technology (regardless of the form in which it is provided), software or software source code, received from TI or any of its affiliates under this Agreement may be under export control of the United States or other countries. You shall comply with the United States and other applicable non-U.S. laws and regulations governing the export, re-export and release of any products, technology, software, or software source code received under this Agreement from TI or its affiliates. You shall not undertake any action that is prohibited by the EAR. Without limiting the generality of the foregoing, you specifically agree that you shall not transfer or release products, technology, software, or software source code of TI or its affiliates to, or for use by, military end users or for use in military, missile, nuclear, biological, or chemical weapons end uses.

(iii). Licenses. Each party shall secure at its own expense, such licenses and export and import documents as are necessary for each respective party to fulfill its obligations under this Agreement. If such licenses or government approvals cannot be obtained, TI may terminate this Agreement, or shall otherwise be excused from the performance of any obligations it may have under this Agreement for which the licenses or government approvals are required.

13. Entire Agreement. This is the entire Agreement between you and TI, and absent a signed and effective software license agreement related to the subject matter of this Agreement, this Agreement supersedes any prior agreement between the parties related to the subject matter of this Agreement. Notwithstanding the foregoing, any signed and effective software license agreement relating to the subject matter hereof will supersede the terms of this Agreement. No amendment or modification of this Agreement will be effective unless in writing and signed by a duly authorized representative of TI. You hereby warrant and represent that you have obtained all authorizations and other applicable consents required empowering you to enter into this Agreement.